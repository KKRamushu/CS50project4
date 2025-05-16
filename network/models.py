from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models


class User(AbstractUser):
    pass

def user_directory(instance, filename):
    return f'user_{instance.user.id}/{filename}'

class User_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory, default='default.jpeg')
    def __self__(self):
        return f"{self.user.username}'s Profile"

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    content = models.CharField(max_length=800)
    timestamp = models.DateTimeField(auto_now_add=False)
    def __str__(self):
        return f"{self.poster.username} posted {self.content}"
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked_post")
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liker")
    def __str__ (self):
        return f"{self.post} is liked by {self.liker.username}"
    
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_user")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_user")
    def __str__ (self):
        return f"{self.follower.username} follows {self.following.username}"