"""
0. User 모델 확장 가능성을 염두하라.
1. $ django-admin startproject MY_PROJECT
2. $ django-admin startapp accounts
3. accounts/models.py => 아래 코드 작성
4. settings.py => INSTALLED APPS += 'accounts'
5. settings.py => AUTH USERMODEL = 'accounts.User'
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings', blank=True)

    def __str__(self):
        return self.username