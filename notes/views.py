from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'notes/index.html')


def profile(request):
    return render(request, 'account/profile.html')
