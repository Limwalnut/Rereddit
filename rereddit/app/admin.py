from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Thread


# Register your models here.
admin.site.register(Thread)