from ws.models import Poll
from ws.models import Question
from ws.models import Option
from ws.models import PollUser

from ws.serializers import PollSerializer

from django.db import transaction

from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status

class PollView(APIView):
    def get_validated(self, obj, field):
        if obj.get(field) == None:
            raise IndexError('{} is not defined in given data'.format(field))
        else:
            return obj.get(field)

    def post(self, req):
        data = JSONParser().parse(req)
        serialized_poll = PollSerializer(data=data)
        if serialized_poll.is_valid():
            poll_object = serialized_poll.save()
            return Response({'msg': 'Poll Created', 'id': poll_object.id},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_poll.errors,
                            status=status.HTTP_400_BAD_REQUEST)
     
    def get(self, req, poll_id=None):
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
    
    def delete(self, req, poll_id):
        try:
            poll_object = Poll.objects.get(pk=poll_id)
            poll_object.delete()
            return Response({'msg': 'Object Deleted'},
                    status=status.HTTP_202_ACCEPTED)
        except Poll.DoesNotExist:
            return Response({'msg': 'Object with given ID does not exist'},
                    status=status.HTTP_400_BAD_REQUEST)