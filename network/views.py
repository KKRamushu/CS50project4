from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from django.utils import timezone
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post, Like, Follow, User_Profile


def index(request):
    # Gets all postings and present them in groups of 10 per page

    allPosts = Post.objects.all().order_by('-timestamp')
    page = request.GET.get('page')
    sortedPosts = Paginator(allPosts, 10).get_page(page)
    return render(request, "network/index.html",{"allPosts":sortedPosts, "profile": False})

def followingPosts(request):
    # Get posts from users that are followed by current user

    following = Follow.objects.filter(follower=request.user).values_list('following', flat=True)  
    followingPosts = Post.objects.filter(poster__in=following).order_by('-timestamp')
    page = request.GET.get('page')
    sortedPosts = Paginator(followingPosts,2).get_page(page)
    return render(request, "network/index.html",{"allPosts":sortedPosts,"profile": False})

# 
def viewProfile(request,posterId):
    # View user posts, followings, and followers

    allPosts = Post.objects.filter(poster=posterId).order_by('-timestamp')
    followers = Follow.objects.filter(following=posterId).count()
    following = Follow.objects.filter(follower=posterId).count()
    posterName = User.objects.get(id=posterId)
    if (request.user.is_authenticated):
        isFollowing = Follow.objects.filter(follower=request.user, following=posterName).exists()
    else:
        isFollowing = False
    page = request.GET.get('page')
    sortedPosts = Paginator(allPosts, 10).get_page(page)
    
    return render(request, "network/index.html",{"profile": True, "allPosts":sortedPosts, "followers": followers,
                                                    "following": following,
                                                   "posterName":posterName, "isFollowing": isFollowing })

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
    
def upload_user_pic(request):
    # Get profile picture from user and save it to user's profile

    if request.method == "POST":
        profile = request.user.user_profile
        profile.image = request.FILES.get('image')
        profile.save()
        return HttpResponseRedirect(viewProfile(request.user.id))

def post(request):
    # Make new posting

    if request.method == "POST":
        poster = request.user
        content = request.POST["post-content"]
        postTime = timezone.now()
        
        newPost = Post(
            poster = poster,
            content = content,
            timestamp = postTime
        )

        newPost.save()
        return HttpResponseRedirect(reverse("index"))

@csrf_exempt
def follow(request):
    # Follow or unfollow a user

    if request.method != 'POST':
        return ({"error":"incorrect request!"})
    follower = request.user
    data = json.loads(request.body)
    userId = data["userId"]
    following = User.objects.get(id= userId)
    followerExist = Follow.objects.filter(follower=follower,following=following)
    if followerExist.exists():
        followerExist.delete()
    else:
        new_follow = Follow(
            follower = follower,
            following = following
        )
        new_follow.save()
    data = {
        "isFollowing": Follow.objects.filter(follower=follower,following=following).exists(),
        "followers": Follow.objects.filter(following=following).count()
        }
    return JsonResponse(data)

def like(request, postId):
    # Like or unlike a post

    post = Post.objects.get(id=postId)
    like = Like.objects.filter(post=post, liker=request.user)
    if like.exists():
        like.delete()
    else:
        new_like = Like(
            post = post,
            liker = request.user
        )
        new_like.save()
    likes = Like.objects.filter(post = post).count()
    data = {'likes':likes,
            'isLiked':like.exists()}
    return JsonResponse(data)

def likes(request, postId):
    # Check if a post is liked and get the total number of likes 

    post = Post.objects.get(id=postId)
    isLiked = Like.objects.filter(post=post, liker=request.user).exists()
    data = {
            "likes": Like.objects.filter(post=post).count(),
            "isLiked": isLiked
        }
    return JsonResponse(data)

def edit(request,postId):
    # fetch post from database and return it as JSON data to page as editable text
    
    post = Post.objects.get(id=postId)
    data = {"id": post.id,
            "poster": post.poster.username,
            "content": post.content}
    return JsonResponse(data, safe=False)

@csrf_exempt
def edited(request, postId):
    # Save edited post

    if request.method != "PUT":
        return ({"error":"incorrect request!"})
    data = json.loads(request.body)
    post = Post.objects.get(id=postId)
    post.content = data["contents"]
    post.timestamp = timezone.now()
    post.save()
    newPost = {"timeStamp": post.timestamp.strftime("%Y-%m-%d %H:%M"),
            "content": post.content}
    return JsonResponse(newPost, safe=False)