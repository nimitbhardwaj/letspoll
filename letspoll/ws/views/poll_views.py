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
    def post(self, req):
        data = JSONParser.parse(req)
        serialized_poll = PollSerializer(data=data)
        if serialized_poll.is_valid():
            poll_object = serialized_poll.save()
            return Response({'id': poll_object.id, 'msg': 'Poll Created'},
                            status=status.HTTP_201_CREATED)

    def get(self, req, poll_id):
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
            poll_object = Poll.object.get(pk=poll_id)
            poll_object.delete()
            return Response({'msg': 'Object Deleted'},
                    status=status.HTTP_202_ACCEPTED)
        except Poll.DoesNotExist:
            return Response({'msg': 'Object with given ID does not exist'},
                    status=status.HTTP_400_BAD_REQUEST)