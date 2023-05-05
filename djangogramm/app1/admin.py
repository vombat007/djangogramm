from django.contrib import admin
from .models import User, Post, Image, PostHashtag, Like

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Image)
admin.site.register(PostHashtag)
admin.site.register(Like)
