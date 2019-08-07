from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from datetime import datetime, timedelta

import uuid
import jwt

# Create your models here.


class Poll(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False)
    name = models.CharField(max_length=200, unique=True, null=False)
    is_secret_poll = models.BooleanField(null=False, default=False)

class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False)
    text = models.CharField(max_length=200, null=False)
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE, null=False)

class Option(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False)
    text = models.CharField(max_length=200, null=False)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, null=False)

