
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("followingPosts", views.followingPosts, name="following"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:poster>", views.viewProfile, name="profile"),
    path("post", views.post, name="post"),
    path("follow", views.follow, name="follow"),
    path("like/", views.like, name="like")
]
