from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from .forms import SignupForm

# Create your views here.

def home(request):
    return render(request, 'website/home.html', {
        "message" : "Login Successful"
    })

def login_user(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            HttpResponseRedirect(reverse('home'))
        else:
            return render(request, 'website/login.html', {
                "message": "Login Failed."
            })

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    else:
        return render(request, 'website/login.html', {})
    
def logout_user(request):
    logout(request)
    return render(request, 'website/login.html', {"message": "Logout Successful"})

def register(request):
    if request.method=="POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
    else:
        form = SignupForm()
        # return render(request, 'website/register.html', {
        #     'form': form
        # })

    return render(request, 'website/register.html', {'form': form})