from ws.models import Poll

from ws.serializers import PollSerializer

from authentication.backends import JWTAuthentication

from django.db import transaction
from django.conf import settings
from django.core.exceptions import ValidationError

from rest_framework import decorators
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import decorators

from itsdangerous import Signer


@decorators.api_view(['post'])
def create_poll(req):
    '''
        create_poll:
            Creates the Poll
    '''
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

@decorators.api_view(['get'])
def get_poll_by_name(req, poll_name):
    print('bye')
    try:
        poll_name = poll_name.replace('-', ' ')
        poll = Poll.objects.filter(name__iexact=poll_name)
        if len(poll) == 0:
            raise Poll.DoesNotExist
        else:
            poll = poll[0]
        if poll.name != poll_name:
            raise Poll.DoesNotExist
        return Response({'id': poll.id}, status=status.HTTP_200_OK)
    except Poll.DoesNotExist:
        return Response({'msg': 'Poll with given name does not exits'},
                        status=status.HTTP_400_BAD_REQUEST)

class PollByIDView(APIView):
    authentication_classes = (JWTAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, req, poll_id):
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

    def delete(self, req, poll_id):
        try:
            poll_object = Poll.objects.get(pk=poll_id)
            poll_object.delete()
            return Response({'msg': 'Object Deleted'},
                    status=status.HTTP_202_ACCEPTED)
        except Poll.DoesNotExist:
            return Response({'msg': 'Object with given ID does not exist'},
                    status=status.HTTP_400_BAD_REQUEST)
