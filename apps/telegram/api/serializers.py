from rest_framework import serializers
from apps.telegram.models import Config, Message

class ConfigSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Config
        fields = [
            'id', 'session_name', 'api_id', 'api_hash', 'access_token', 'bot_token', 'is_bot', 'is_active', 'is_ready'
        ]


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = [
            'app', 'message_id', 'message_type', 'text', 'sender_id', 'sender_username', 'sender_first_name',
            'sender_last_name', 'sender_recently_status', 'sender_is_bot', 'sender_is_contact', 'sender_is_scam',
            'sender_is_support', 'chat_id', 'chat_type', 'chat_title', 'chat_username',
        ]

