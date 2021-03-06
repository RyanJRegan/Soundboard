from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django import forms
from django.http import JsonResponse
from soundboard.models import Sound, Soundboard, SoundboardAssociation
import json
from django.http import HttpResponse

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

def index(request):
    return render(request, "soundboard/index.html")

@csrf_protect
def login_user(request):
    if request.method != 'POST':
        return redirect('/login_or_signup/')
    authentication_form = AuthenticationForm(data=request.POST)
    if not authentication_form.is_valid():
        return login_or_signup(request, authentication_form=authentication_form)
    username = authentication_form.cleaned_data.get('username')
    password = authentication_form.cleaned_data.get('password')
    user = authenticate(username=username, password=password)
    login(request, user)
    return redirect('your_boards')

@csrf_protect
def signup(request):
    if request.method != 'POST':
        return redirect('/login_or_signup/')
    user_creation_form = SignUpForm(data=request.POST)
    if not user_creation_form.is_valid():
        return login_or_signup(request, user_creation_form=user_creation_form)
    user_creation_form.save()
    username = user_creation_form.cleaned_data.get('username')
    password = user_creation_form.cleaned_data.get('password1')
    user = authenticate(username=username, password=password)
    login(request, user)
    return redirect('your_boards')

def login_or_signup(request, authentication_form=None, user_creation_form=None):
    if authentication_form is None:
        authentication_form = AuthenticationForm()
    if user_creation_form is None:
        user_creation_form = SignUpForm()
    return render(request, "soundboard/login_or_signup.html", {'authentication_form': authentication_form,
        'user_creation_form': user_creation_form})

@login_required
def your_boards(request):
    return render(request, "soundboard/your_boards.html")

@login_required
def new_board(request):
    existing_sounds = []
    for sound in request.user.sound_set.all():
        existing_sounds.append(sound.as_dict())
    return render(request, "soundboard/new_board.html", {
        'existing_sounds': json.dumps( existing_sounds)
    })

def create_sound(request):
    new_sound = Sound.objects.create(name=request.POST.get('name'),
            text=request.POST.get('text'),
            image_file=request.FILES.get('image_file'),
            sound_file=request.FILES.get('sound_file'),
            user=request.user)

    return JsonResponse(new_sound.as_dict())

def create_soundboard(request):
    sounds_to_be_added = request.POST.get('sounds').split(',')
    soundboard_name = request.POST.get('soundboardName')

    soundboard = Soundboard.objects.create(name=soundboard_name,
                                           user=request.user)
    # import pdb; pdb.set_trace()
    for i, sound_id in enumerate(sounds_to_be_added):
        # pdb.set_trace()
        sound = get_object_or_404(Sound, id=sound_id) # may have to convert sound_id to int
        soundboard_association = SoundboardAssociation.objects.create(
                sound=sound,
                soundboard=soundboard,
                order=i)
        soundboard_association.save()

    return JsonResponse({ 'id': soundboard.id })

    # import pdb; pdb.set_trace(),
    # soundboard = SoundboardAssociation(sounds=sounds_to_be_added, 
    # return render(request, "soundboard/your_boards.html")

def show_soundboard(request, id=None):
    soundboard = get_object_or_404(Soundboard, id=int(id))

    return render(request, "soundboard/show_soundboard.html", {
        'soundboard': json.dumps(soundboard)
    })
