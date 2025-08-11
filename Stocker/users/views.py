from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, transaction
from django.contrib import messages
from .models import Profile
from products.models import Category 


def sign_up(request: HttpRequest ):

    if request.method == "POST":

        try:
            with transaction.atomic():
                new_user = User.objects.create_user(username=request.POST["username"],password=request.POST["password"],email=request.POST["email"], first_name=request.POST["first_name"], last_name=request.POST["last_name"])
                new_user.save()

                profile = Profile(user=new_user, about=request.POST["about"],  avatar=request.FILES.get("avatar", Profile.avatar.field.get_default()) ,phone =request.POST["phone"])
                profile.save()

            messages.success(request, "Registered User Successfuly")
            return redirect("users:sign_in")
        
        except IntegrityError as e:
            messages.error(request, "Please choose another username")
        except Exception as e:
            messages.error(request, "Couldn't register user. Try again")
            print(e)
    

    return render(request, "users/signup.html")



def sign_in(request: HttpRequest):
    if request.method == "POST":
        user = authenticate(request,
                            username=request.POST.get("username"),
                            password=request.POST.get("password"))

        if user:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect(request.GET.get("next", "/"))
        else:
            messages.error(request, "Incorrect username or password. Please try again.")

    return render(request, "users/signin.html")


def log_out(request: HttpRequest):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect(request.GET.get("next", "/"))



def update_user_profile(request: HttpRequest):
    if not request.user.is_authenticated:
        messages.warning(request, "Only registered users can update their profile")
        return redirect("users:sign_in")

    user = request.user
    profile = Profile.objects.filter(user=user).first()

    if not profile:
        profile = Profile(user=user)
        profile.save()

    if request.method == "POST":
        try:
            with transaction.atomic():
                user.first_name = request.POST.get("first_name", user.first_name)
                user.last_name = request.POST.get("last_name", user.last_name)
                user.email = request.POST.get("email", user.email)
                user.save()

                profile.about = request.POST.get("about", profile.about)
                profile.phone = request.POST.get("phone", profile.phone)
                profile.category = Category.objects.filter(pk=request.POST.get("category")).first()
                if "avatar" in request.FILES:
                    profile.avatar = request.FILES["avatar"]
                profile.save()

                messages.success(request, "Updated profile successfully", "alert-success")
        except Exception as e:
            print(e)
            messages.error(request, "Couldn't update profile", "alert-danger")

    categories = Category.objects.all()
    return render(request, "users/update_profile.html", {
        "user": user,
        "profile": profile,
        "categories": categories
    })


def user_profile_view(request: HttpRequest, user_name: str):
    try:
        user = User.objects.get(username=user_name)
        profile = Profile.objects.filter(user=user).first()

        if not profile:
            profile = Profile(user=user)
            profile.save()

    except Exception as e:
        print(e)
        return render(request, '404.html')

    return render(request, 'users/profile.html', {"user": user, "profile": profile})
