from rest_framework import serializers

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
    class Meta:
        model = Poll
        fields = ('id', 'name', 'questions', 'is_secret_poll')
        read_only_fields = ('id',)