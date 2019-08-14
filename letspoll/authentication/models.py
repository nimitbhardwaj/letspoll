from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from datetime import datetime, timedelta

import uuid
import jwt

from ws.models import Poll

# Create your models here.


class PollUserManager(BaseUserManager):
    def create_user(self, username, password, poll):
        if username is None:
            raise TypeError('Username should not be None')
        if password is None:
            raise TypeError('Password should not be None')
        user = self.model(username=username,
                            poll=poll,
                            status='PN',
                            is_admin=False)
        user.set_password(password)
        user.save()
        return user
    
    def get_user_by_name(self, username, poll):
        user = self.get(username=username, poll=poll)
        return user

class PollUser(AbstractBaseUser, PermissionsMixin):
    USER_STATUS = [
        ('PN', 'Pending'),
        ('AP', 'Approved'),
        ('RJ', 'Rejected')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False)
    username = models.CharField(max_length=200, null=False)
    password = models.CharField(max_length=200, null=False)
    poll = models.ForeignKey('ws.Poll', on_delete=models.CASCADE, null=False)
    status = models.CharField(choices=USER_STATUS, default='PN', max_length=20, null=False)
    is_admin = models.BooleanField(default=False, null=False)

    USERNAME_FIELD='id'
    REQUIRED_FIELDS = ['username', 'poll', 'password']
    objects = PollUserManager()

    def __str__(self):
        return self.username
    
    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': str(self.pk),
            'exp': int(dt.strftime('%s')),
            'poll_id': str(self.poll.id),
            'is_admin': self.is_admin,
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

    class Meta:
        unique_together = ('poll', 'username')
