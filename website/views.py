from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import SignupForm, AddRecordForm
from .models import Record

# Create your views here.


def home(request):
    records = Record.objects.all()
    if not request.user.is_authenticated:
        messages.success(request, "Please login first.")
        return HttpResponseRedirect(reverse("login"))
    return render(request, 'website/home.html', {
        "records": records
    })

def login_user(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # HttpResponseRedirect(reverse('home'))
        else:
            return render(request, 'website/login.html', {
                "message": "Login Failed. Please Try Again."
            })

    if request.user.is_authenticated:
        messages.success(request, "Login Successful.")
        return HttpResponseRedirect(reverse("home"))
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
            messages.success(request, "welcome! Registration Successful.")
            return HttpResponseRedirect(reverse("home"))
    else:
        form = SignupForm()
        # return render(request, 'website/register.html', {
        #     'form': form
        # })

    return render(request, 'website/register.html', {'form': form})

def view_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id = pk)
        return render(request, 'website/record.html', {
            "record": record
        })
    else:
        messages.warning(request, "You do not have the permission. Please Login First.")
        return HttpResponseRedirect(reverse("login"))
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id = pk)
        record.delete()
        messages.success(request, "Record Deleted Successfully.")
        return HttpResponseRedirect(reverse('home'))
    else:
        messages.warning(request, "You do not have the permission. Please Login First.")
        return HttpResponseRedirect(reverse('login'))
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method=='POST':
            if form.is_valid:
                form.save()
                messages.success(request, "Record Added Successfully.")
                return HttpResponseRedirect(reverse('home'))
        return render(request, 'website/add.html', {'form': form})
    else:
        messages.warning(request, "You are not authorized. Please Login First.")
        return HttpResponseRedirect(reverse('login'))
    
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if request.method=="POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Record Updated Successfully.")
                return HttpResponseRedirect(reverse("home"))
        return render(request, 'website/update.html', {'form': form})
    else:
        messages.error(request, "You must be logged in for this action.")
        return HttpResponseRedirect(reverse("login"))