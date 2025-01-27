from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime

from .models import User, Post, Likes, Follow


def index(request):
    allPosts = Post.objects.all()
    sortedPosts = sorted(allPosts, key=lambda allPosts: allPosts.timestamp, reverse=True)
    return render(request, "network/index.html",{"allPosts":sortedPosts})

def viewProfile(request,poster):
    allPosts = Post.objects.filter(poster=poster)

    followers = len(Follow.objects.filter(following=poster))
    following = len(Follow.objects.filter(follower=poster))
    posterName = User.objects.get(id=poster)
    sortedPosts = sorted(allPosts, key=lambda allPosts: allPosts.timestamp, reverse=True)
    
    return render(request, "network/profile.html",{"userPosts":sortedPosts, "followers": followers, "following": following,
                                                   "posterName":posterName })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def post(request):
    if request.method == "POST":
        poster = request.user
        content = request.POST["post-content"]
        postTime = datetime.now().strftime("%d-%m-%Y %H:%M")
        
        newPost = Post(
            poster = poster,
            content = content,
            timestamp = postTime
        )

        newPost.save()
        return (index(request))

def follow(request):
    if request.method == 'POST':
        follower = User.objects.get(id=request.POST['follower'])
        following = User.objects.get(id=request.POST['following'])
        follow = Follow(
            follower = follower,
            following = following
        )
        follow.save()
        return viewProfile(request,following.id)
