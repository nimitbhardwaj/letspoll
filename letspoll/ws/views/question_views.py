from ws.models import Poll
from ws.models import Question
from ws.models import Option
from ws.models import PollUser

from ws.serializers import QuestionSerializer

from django.db import transaction

from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status

class QuestionView(APIView):
    def get_validated(self, obj, field):
        if obj.get(field) == None:
            raise IndexError('{} is not defined in given data'.format(field))
        else:
            return obj.get(field)

    def post(self, req, poll_id):
        try:
            data = JSONParser().parse(req)
            poll_object = Poll.objects.get(pk=poll_id)
            serialized_question = QuestionSerializer(data={**data,
                                    **{'poll': poll_object.id}})
            if serialized_question.is_valid():
                question_object = serialized_question.save()
                return Response({'msg': 'Question created success',
                                'id': question_object.id}, status=status.HTTP_201_CREATED)
            else:
                return Response(serialized_question.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except Poll.DoesNotExist:
            return Response({'msg': 'Object with given ID does not exist'},
                                status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, req, poll_id, question_id=None):
        if question_id == None or question_id == '':
            question_objects = Question.objects.filter(poll_id=poll_id)
            serialized_question = QuestionSerializer(question_objects, many=True)
            return Response(serialized_question.data,
                                status=status.HTTP_200_OK)

        else:
            try:
                poll_object = Poll.objects.get(pk=poll_id)
                question_object = Question.objects.get(pk=question_id)
                serialized_question = QuestionSerializer(question_object)
                return Response(serialized_question.data,
                                status=status.HTTP_200_OK)
            except Poll.DoesNotExist:
                return Response({'msg': 'Poll Object with given ID does not exist'},
                        status=status.HTTP_400_BAD_REQUEST)
            except Question.DoesNotExist:
                return Response({'msg': 'Question Object with given ID does not exist'},
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, req, poll_id, question_id):
        try:
            poll_object = Poll.objects.get(pk=poll_id)
            question_object = Question.objects.get(pk=question_id)
            question_object.delete()
            return Response({'msg': 'Object deleted success'},
                    status=status.HTTP_202_ACCEPTED)
        except Poll.DoesNotExist:
            return Response({'msg': 'Poll Object with given ID does not exist'},
                    status=status.HTTP_400_BAD_REQUEST)
        except Question.DoesNotExist:
            return Response({'msg': 'Question Object with given ID does not exist'},
                    status=status.HTTP_400_BAD_REQUEST)



