from django.db import models

# Create your models here.


class UserModel(models.Model):
    username = models.CharField(max_length=16)
    email = models.EmailField()
    password = models.CharField(max_length=16)


class UserSession(models.Model):
    userID = models.CharField(max_length=2)
    authKey = models.CharField(max_length=8)
    lastLoggedIn = models.DateTimeField()
