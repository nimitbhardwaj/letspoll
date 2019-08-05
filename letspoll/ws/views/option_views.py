from ws.models import Poll
from ws.models import Question
from ws.models import Option
from ws.models import PollUser

from ws.serializers import OptionSerializer

from django.db import transaction

from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status

class OptionView(APIView):
    def get_validated(self, obj, field):
        if obj.get(field) == None:
            raise IndexError('{} is not defined in given data'.format(field))
        else:
            return obj.get(field)

    def post(self, req, poll_id, question_id):
        try:
            data = JSONParser().parse(req)
            question_object = Question.objects.get(pk=question_id)
            assert question_object.poll.id == poll_id
            serialized_option = OptionSerializer(data={**data,
                                    **{'question_id': question_object.id}})
            if serialized_option.is_valid():
                option_object = serialized_option.save()
                return Response({'msg': 'Option created success',
                                'id': question_object.id}, status=status.HTTP_201_CREATED)
            else:
                return Response(serialized_question.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except Poll.DoesNotExist:
            return Response({'msg': 'Poll Object with given ID does not exist'},
                                status=status.HTTP_400_BAD_REQUEST)
        except Question.DoesNotExist:
            return Response({'msg': 'Question Object with given ID does not exist'},
                                status=status.HTTP_400_BAD_REQUEST)
        except AssertionError:
            return Response({'msg': 'No questionID with given pollID'},
                                status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, req, poll_id, question_id, option_id=None):
        if option_id == None or option_id == '':
            try:
                option_objects = Option.objects.filter(question_id=question_id)
                if len(option_objects) != 0:
                    assert str(option_objects[0].question.poll.id) == str(poll_id)
                serialized_options = OptionSerializer(option_objects, many=True)
                return Response(serialized_options.data, status=status.HTTP_200_OK)
            except:
                return Response({'msg': 'Object with given IDs does not exist'},
                                status=status.HTTP_200_OK)
        else:
            try:
                option_object = Option.objects.get(pk=option_id)
                assert str(option_object.question.id) == question_id
                assert str(option_object.question.poll.id) == poll_id
                serialized_option = OptionSerializer(option_object)

                return Response(serialized_option.data, status=status.HTTP_200_OK)
            except Option.DoesNotExist:
                return Response({'msg': 'Object with given OptionID does not exist'},
                                status=status.HTTP_200_OK)
            except AssertionError:
                return Response({'msg': 'Object with given poll ID or question ID does not exist'},
                                status=status.HTTP_200_OK)
    
    def delete(self, req, poll_id, question_id, option_id):
        try:
            option_object = Option.objects.get(pk=option_id)
            assert str(option_object.question.id) == question_id
            assert str(option_object.question.poll.id) == poll_id
            option_object.delete()
        except Option.DoesNotExist:
            return Response({'msg': 'Object with given OptionID does not exist'},
                            status=status.HTTP_200_OK)
        except AssertionError:
            return Response({'msg': 'Object with given poll ID or question ID does not exist'},
                            status=status.HTTP_200_OK)

