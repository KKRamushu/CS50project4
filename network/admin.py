from django.contrib import admin

# Register your models here.

from .models import User_Profile, Post, Like,Follow

admin.site.register(User_Profile)
admin.site.register(Like)
admin.site.register(Post)
admin.site.register(Follow)