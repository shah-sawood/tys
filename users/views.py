"""All accounts are managed from here"""
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

import os

from .forms import LoginForm
from .forms import ProfileForm
from .forms import RegistrationForm
from .forms import UpdateBioForm
from .forms import UpdatePersonalInfoForm
from .forms import UpdateProfilePictureForm
from .models import Notification
from .models import Profile
from .models import SocialLink

from tests.decorators import is_admin

# login user
def login_view(request):
    """authenticate & login user"""
    if not request.user.is_authenticated:
        context = {"title": "Login"}
        # when method is POST
        if request.method == "POST":
            login_form = LoginForm(request.POST)
            # check form validity
            if login_form.is_valid():
                username = login_form.cleaned_data["username"].lower()
                password = login_form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                # when credentials are invalid
                if user is None:
                    messages.error(request, "Invalid username and/or password.")
                    return HttpResponseRedirect(reverse("users:login"))
                login(request, user)  # login user
                if request.POST.get("next"):
                    return HttpResponseRedirect(request.POST.get("next"))
                elif request.user.is_superuser:
                    return HttpResponseRedirect(reverse("superuser:index"))
                return HttpResponseRedirect(reverse("index"))
            # when form is invalid
            messages.error(request, "Something went wrong. Please try again later.")
            return HttpResponseRedirect(request.META.get("HTTP_REFERRER", "/"))
        return render(request, "users/login.html", context)  # when method is GET
    else:
        return HttpResponseRedirect(request.META.get("HTTP_REFERRER", "/"))


# logout user
def logout_view(request):
    """logout user"""
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# register new user
def register_view(request):
    context = {"title": "Register"}

    if request.method == "POST":

        # ensure user sends username, first_name, last_name
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        # Ensure password matches confirmation
        password = request.POST.get("password1")
        confirmation = request.POST.get("password2")

        # put the data into context dictionary
        context["username"] = username
        context["first_name"] = first_name
        context["last_name"] = last_name
        if username and "@" in username:
            if first_name:
                if last_name:
                    if password and confirmation:
                        if password != confirmation:
                            messages.error(request, "Passwords must match.")
                        else:
                            # Attempt to create new user
                            try:
                                user = User.objects.create_user(
                                    username=username,
                                    email=username,
                                    first_name=first_name,
                                    last_name=last_name,
                                    password=password,
                                )
                                user.save()
                            except IntegrityError:
                                messages.error(request, "Email address already taken.")
                            else:
                                login(request, user)
                                return HttpResponseRedirect(
                                    reverse("users:profile", args=[user.id])
                                )
                    else:
                        messages.error(request, "Passwords can't be empty.")
                else:
                    messages.error(request, 'Last name can"t be empty.')
            else:
                messages.error(request, 'First name can"t be empty.')
        else:
            messages.error(request, 'Email can"t be empty.')
        return render(request, "users/register.html", context)

    return render(request, "users/register.html", context)


# user profile
@require_http_methods(["GET"])
def profile(request, user_id):
    """manage user profile"""
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        messages.error(request, "Something went wrong. Please try again later.")
        return HttpResponseRedirect(request.META.get("HTTP_REFERRER", "/"))

    context = {
        "user": user,
        "title": f"Profile | {user.username}",
        "is_owner": user.id == request.user.id,
    }
    return render(request, "users/profile.html", context)


@login_required
@require_http_methods(["GET"])
def update_profile(request):
    return render(
        request,
        "users/update-profile.html",
        {
            "form": UpdateProfilePictureForm(),
            "title": f"Settings - {request.user.get_username()}",
        },
    )


@login_required
@require_http_methods(["GET", "POST"])
def update_profile_picture(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        user = request.user
    form = UpdateProfilePictureForm(request.POST, request.FILES, instance=user.profile)
    old = user.profile.get_profile_pic().url
    if form.is_valid():
        form.save()
        if old[1:].split("/")[-1] != "default.jpg":
            try:
                os.remove(old[1:])
            except FileNotFoundError:
                pass
        messages.success(request, "profile picture updated successfully.")
    else:
        messages.error(request, "Something went wrong. Please try again later.")
    return HttpResponseRedirect(reverse("users:profile", args=[user.id]))


@login_required
@require_http_methods(["POST"])
def update_personal_info(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        user = request.user
    form = UpdatePersonalInfoForm(request.POST, instance=user)
    if form.is_valid():
        form.save()
        messages.success(request, "Personal Information updated successfully.")
    else:
        messages.error(request, "Something went wrong. Please try again later.")
    return HttpResponseRedirect(request.META.get("HTTP_REFERRER", "/"))


@login_required
@require_http_methods(["POST"])
def update_bio(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        user = request.user
    bio_form = UpdateBioForm(request.POST, instance=user.profile)
    if bio_form.is_valid():
        bio_form.save()
        messages.success(request, "Bio updated successfully.")
    else:
        messages.error(request, "Something thing went wrong. Please try again later.")
    return HttpResponseRedirect(reverse("users:profile", args=[user.id]))
