from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from django.contrib.auth import get_user_model

from authentication.models import PollUser

from ws.models import Poll



class CreatePollUserSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255, read_only=True)
    user_id = serializers.UUIDField(source='id', read_only=True)
    poll_id = serializers.PrimaryKeyRelatedField(source='poll', queryset=Poll.objects.all())
    class Meta:
        model = PollUser
        fields = ('user_id', 'username', 'password', 'poll_id', 'status', 'is_admin', 'token')
        read_only_fields = ('status', 'is_admin')
    
    def create(self, validated_data):
        return PollUser.objects.create_user(**validated_data)
    
class LoginPollUserSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    poll_id = serializers.CharField(max_length=100, write_only=True)
    token = serializers.UUIDField(read_only=True)
    user_id = serializers.UUIDField(read_only=True)

    def validate(self, data):
        """
        Validates user data.
        """
        username = data.get('username', None)
        password = data.get('password', None)
        poll = data.get('poll_id', None)

        if username is None:
            raise serializers.ValidationError(
                'A Username is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        
        if poll == None:
            raise serializers.ValidationError(
                'A PollID is required to log in.'
            )
        else:
            try:
                poll = Poll.objects.get(pk=poll)
            except Poll.DoesNotExist:
                raise serializers.ValidationError(
                    'Poll with given ID does not exist.'
                )

        user = PollUser.objects.get_user_by_name(username, poll)

        if user is None:
            raise serializers.ValidationError(
                'User with given credentials not found'
            )
        if not user.check_password(password):
            raise serializers.ValidationError(
                'Invalid Password for the user'
            )
        return {
            'token': user.token,
            'user_id': user.id
        }