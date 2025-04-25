
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("followingPosts", views.followingPosts, name="following"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:posterId>", views.viewProfile, name="profile"),
    path("post", views.post, name="post"),
    path("follow/", views.follow, name="follow"),
    path("like/<int:postId>", views.like, name="like"),
    path("likes/<int:postId>", views.likes, name="likes"),
    path("edit/<int:postId>", views.edit, name="edit"),
    path("edited/<int:postId>", views.edited, name="edited")
]
