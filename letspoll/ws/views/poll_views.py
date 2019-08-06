from ws.models import Poll

from ws.serializers import PollSerializer

from authentication.backends import JWTAuthentication

from django.db import transaction
from django.conf import settings
from django.core.exceptions import ValidationError

from rest_framework.viewsets import ViewSet
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from itsdangerous import Signer


class PollView(ViewSet):
    authentication_classes = (JWTAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def standardize_poll_name(self, poll_name):
        return poll_name.replace(' ', '-')

    def create_poll(self, req):
        data = JSONParser().parse(req)
        serialized_poll = PollSerializer(data=data)
        if serialized_poll.is_valid():
            poll_object = serialized_poll.save()
            signer = Signer(settings.HASH_SECRET_KEY)
            secret_token = signer.sign(str(poll_object.id))

            return Response({'msg': 'Poll Created',
                            'id': poll_object.id,
                            'secret_token': secret_token},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_poll.errors,
                            status=status.HTTP_400_BAD_REQUEST)
     
    def get_poll_by_id(self, req, poll_id=None):
        if poll_id == '' or poll_id == None:
            serialized_polls = PollSerializer(
                Poll.objects.all(),
                many=True
            )
            return Response(serialized_polls.data, status=status.HTTP_200_OK)
        else:
            try:
                serialized_poll = PollSerializer(
                    Poll.objects.get(pk=poll_id)
                )
                return Response(serialized_poll.data, status=status.HTTP_200_OK)
            except Poll.DoesNotExist:
                return Response({'msg': 'Object with given ID does not exist'},
                                status=status.HTTP_400_BAD_REQUEST)
            except ValidationError:
                return Response({'msg': 'Invalid UID'}, status=status.HTTP_400_BAD_REQUEST)

    def get_poll_by_name(self, req, poll_name):
        try:
            poll_name = poll_name.replace('_', ' ')
            poll = Poll.objects.get(name=poll_name)
            return Response({'exists': True, 'id': poll.id}, status=status.HTTP_200_OK)
        except Poll.DoesNotExist:
            return Response({'msg': 'Poll with given name does not exits', 'exists': False},
                            status=status.HTTP_400_BAD_REQUEST)
    
    def delete_poll(self, req, poll_id):
        try:
            poll_object = Poll.objects.get(pk=poll_id)
            poll_object.delete()
            return Response({'msg': 'Object Deleted'},
                    status=status.HTTP_202_ACCEPTED)
        except Poll.DoesNotExist:
            return Response({'msg': 'Object with given ID does not exist'},
                    status=status.HTTP_400_BAD_REQUEST)