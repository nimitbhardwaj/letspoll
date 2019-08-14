from authentication.models import PollUser

from authentication.serializers import CreatePollUserSerializer, LoginPollUserSerializer

from django.db import transaction
from django.conf import settings
from django.contrib.auth.hashers import make_password

from rest_framework.viewsets import ViewSet
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status

from itsdangerous import Signer
from itsdangerous.exc import BadSignature

class UserView(ViewSet):
    def create_user(self, req):
        data = JSONParser().parse(req)
        serialized_poll_user = CreatePollUserSerializer(data=data)
        if serialized_poll_user.is_valid():
            poll_user_object = serialized_poll_user.save()
            return Response({'msg': 'User created success',
                            'user_id': poll_user_object.id},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_poll_user.errors, status=status.HTTP_400_BAD_REQUEST)

    def make_admin(self, req):
        data = JSONParser().parse(req)
        signer = Signer(settings.HASH_SECRET_KEY)
        poll_id = data['poll_id']
        uid = data['user_id']
        secret_token = data['secret_token']
        try:
            unsigned_data = signer.unsign(secret_token).decode('ascii')
            if unsigned_data == poll_id:
                poll_user_object = PollUser.objects.get(pk=uid)
                poll_user_object.is_admin = True
                poll_user_object.status = 'AP'
                poll_user_object.save()
                return Response({'msg': 'User is now superadmin for given poll'},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({'msg': 'Invalid poll user combo'},
                                status=status.HTTP_400_BAD_REQUEST)
        except BadSignature:
            return Response({'msg': 'Corrupted secret token'},
                                status=status.HTTP_400_BAD_REQUEST)
        except PollUser.DoesNotExist:
            return Response({'msg': 'User with given ID does not exist'},
                                status=status.HTTP_400_BAD_REQUEST)
    
    def login_user(self, req):
        data = JSONParser().parse(req)
        serialized = LoginPollUserSerializer(data=data)
        if serialized.is_valid():
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized.errors, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)