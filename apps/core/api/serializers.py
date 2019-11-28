from rest_framework import serializers
# from django.contrib.auth import get_user_model
from apps.core.models import User
from apps.telegram.models import Message


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'is_staff']

class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = (
            'id',
            'message_id',
            'text',
            'sender_id',
            'sender_username',
            'sender_first_name',
            'sender_last_name',
            'sender_recently_status',
            'sender_is_bot',
            'sender_is_contact',
            'sender_is_scam',
            'sender_is_support',
            'chat_id',
            'chat_type',
            'chat_title',
            'chat_username',
        )
