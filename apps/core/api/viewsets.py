from rest_framework import viewsets
from apps.core.models import User
from apps.telegram.models import Message
from apps.core.api.serializers import (
    UserSerializer, MessageSerializer
)


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer