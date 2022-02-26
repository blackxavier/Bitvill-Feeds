from django.contrib import admin
from feeds.models import User, Report, Post
from django.contrib.auth.admin import UserAdmin

admin.site.register(User, UserAdmin)
admin.site.register(Report)
admin.site.register(Post)
