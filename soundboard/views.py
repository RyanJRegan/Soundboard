from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "soundboard/index.html")

def login(request):
    return render(request, "soundboard/login.html")

@login_required
def your_boards(request):
    return render(request, "soundboard/your_boards.html")
