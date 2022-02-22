from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    avatar = models.ImageField(upload_to='avatar/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.username