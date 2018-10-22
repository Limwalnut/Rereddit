from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Thread,FollowTag,Tag


# Register your models here.
admin.site.register(Thread)
admin.site.register(FollowTag)
admin.site.register(Tag)