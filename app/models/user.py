from django.db import models
from django.contrib.auth.models import User


class User(models.Model):
    user = models.OneToOneField(User)
