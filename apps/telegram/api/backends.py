from apps.telegram.api.serializers import ConfigSerializer, MessageSerializer
from apps.telegram.models import Config
from apps.telegram.middlewares import TriggerMiddleware
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

trigger = TriggerMiddleware()

@api_view(['GET'])
def get_config(request, id, token, format=None):
    if request.method == "GET":
        try:
            config = Config.objects.get(id=id)
            if str(token) == str(config.access_token):
                serializer = ConfigSerializer(config)
                return Response(serializer.data)
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        except Config.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@trigger.message
def create_message(request):
    if request.method == "POST":
        try:
            id = request.data['id']
            access_token = request.data['access_token']
            config = Config.objects.get(id=id)

            if str(access_token) == str(config.access_token):
                serializer = MessageSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_403_FORBIDDEN)

            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        except Config.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
