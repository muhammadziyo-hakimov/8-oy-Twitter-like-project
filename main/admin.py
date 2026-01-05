from django.contrib import admin
from .models import User, UserConfirmation, Post, Media, Comment

admin.site.register([User, UserConfirmation, Post, Media, Comment])
