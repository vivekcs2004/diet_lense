from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    phone = models.CharField(max_length=15,unique=True)

class Profile(models.Model):

    owner = models.OneToOneField(User,)
