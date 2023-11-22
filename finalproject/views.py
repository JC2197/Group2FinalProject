from django.shortcuts import render
from .forms import *
# Create your views here.


def search(request):
    return render(request,'search-results.html')


def signup(request):
    form = SignUpForm(request.POST or None)
    context = {'form': form}
    return render(request, 'landing.html', context)


def signin(request):
    form = SignInForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return render(request, 'search-results.html')