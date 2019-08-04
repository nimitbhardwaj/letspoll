from django.db import models

import uuid
# Create your models here.


class Poll(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False)
    name = models.CharField(max_length=200, unique=True, null=False)

class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False)
    text = models.CharField(max_length=200, null=False)
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE, null=False)

class Option(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False)
    text = models.CharField(max_length=200, null=False)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, null=False)

class User(models.Model):
    USER_STATUS = [
        ('PN', 'Pending'),
        ('AP', 'Approved'),
        ('RJ', 'Rejected')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False)
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE, null=False)
    handle = models.CharField(max_length=200, null=False)
    status = models.CharField(choices=USER_STATUS, default='PN', max_length=20, null=False)
    password = models.CharField(max_length=200, null=False)
    is_admin = models.BooleanField(default=False, null=False)

    class Meta:
        unique_together = ('poll', 'handle')
