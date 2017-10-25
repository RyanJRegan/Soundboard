from django.shortcuts import render


def index(request):
    return render(request, "soundboard/index.html")

def login(request):
    return render(request, "soundboard/login.html")
