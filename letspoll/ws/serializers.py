from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth import get_user_model

from ws.models import Poll
from ws.models import Question
from ws.models import Option

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('id', 'text', 'question')

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True, source='option_set')
    class Meta:
        model = Question
        fields = ('id', 'text', 'poll', 'options')

class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True, source='question_set')
    poll_id = serializers.UUIDField(source='id', read_only=True)
    poll_name = serializers.CharField(source='name',
                    validators=[UniqueValidator(queryset=Poll.objects.all())])
    class Meta:
        model = Poll
        fields = ('poll_id', 'poll_name', 'questions', 'is_secret_poll')
