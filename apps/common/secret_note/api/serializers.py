from rest_framework import serializers
from apps.common.secret_note.models import Note


class NoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Note
        fields = [
            'id', 'text', 'access_token', 'is_viewed', 'timestamp'
        ]
