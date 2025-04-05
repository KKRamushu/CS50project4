from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Like, Follow


def index(request):
    allPosts = Post.objects.all()
    sortedPosts = allPosts.order_by('-timestamp')
    return render(request, "network/index.html",{"allPosts":sortedPosts})

def followingPosts(request):
    following = Follow.objects.filter(follower=request.user).values_list('following', flat=True)  
    followingPosts = Post.objects.filter(poster__in=following).order_by('timestamp')
    return render(request, "network/index.html",{"allPosts":followingPosts})

def viewProfile(request,poster):
    allPosts = Post.objects.filter(poster=poster)

    followers = len(Follow.objects.filter(following=poster))
    following = len(Follow.objects.filter(follower=poster))
    posterName = User.objects.get(id=poster)
    if (request.user.is_authenticated):
        isFollowing = Follow.objects.filter(follower=request.user, following=posterName).exists()
    else:
        isFollowing = False
    sortedPosts = allPosts.order_by('timestamp')
    
    return render(request, "network/profile.html",{"userPosts":sortedPosts, "followers": followers,
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

def post(request):
    if request.method == "POST":
        poster = request.user
        content = request.POST["post-content"]
        postTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        newPost = Post(
            poster = poster,
            content = content,
            timestamp = postTime
        )

        newPost.save()
        return (index(request))

def follow(request):
    if request.method == 'POST':
        follower = request.user
        following = User.objects.get(id=request.POST['following'])
        followerExist = Follow.objects.filter(follower=follower,following=following)
        if followerExist.exists():
            followerExist.delete()
        else:
            follow = Follow(
                follower = follower,
                following = following
            )
            follow.save()
        return viewProfile(request,following.id)

def like(request, postId):
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
    post = Post.objects.get(id=postId)
    isLiked = Like.objects.filter(post=post, liker=request.user).exists()
    data = {
            "likes": Like.objects.filter(post=post).count(),
            "isLiked": isLiked
        }
    return JsonResponse(data)

def edit(request,postId):
    # fetch post fron database and return it as JSON data to page
    
    post = Post.objects.get(id=postId)
    data = {"id": post.id,
            "poster": post.poster.username,
            "content": post.content}
    return JsonResponse(data, safe=False)

@csrf_exempt
def edited(request, postId):
    if request.method != "PUT":
        return ({"error":"incorrect request!"})
    data = json.loads(request.body)
    post = Post.objects.get(id=postId)
    post.content = data["contents"]
    post.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    post.save()
    newPost = {"timeStamp": post.timestamp,
            "content": post.content}
    return JsonResponse(newPost, safe=False)