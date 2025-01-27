from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    content = models.CharField(max_length=800)
    timestamp = models.CharField(max_length=20, null=True, blank=True)
    def __str__(self):
        return f"{self.poster}, {self.content}, {self.timestamp}"
    
class Likes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post")
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liker")
    def __str__ (self):
        return f"{self.post}, {self.liker}"
    
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    def __str__ (self):
        return f"{self.follower}, {self.following}"