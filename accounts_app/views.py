from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import login
from django.contrib import messages
from .models import Profile
# Create your views here.


def registerUser(request):
    form = RegistrationForm
    form_profile = ProfileForm()

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        form_profile = ProfileForm(request.POST)
        if form.is_valid() and form_profile.is_valid():
            user = form.save()
            profile = form_profile.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            messages.success(request, "Welcome!")
            return redirect("home")
    context = {
        "form": form,
        "form_profile": form_profile
    }
    return render(request, "accounts_app/register.html", context)
