from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.telegram.models import Message
from apps.core.api.serializers import MessageSerializer


@api_view(['POST'])
def create_message(request):
    if request.method == "POST":
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def telegram_users(request, format=None):
#     if request.method == "GET":
#         users = TelegramUser.objects.all()
#         serializer = TelegramUserSerializer(users, many=True)
#         return Response(serializer.data)


# @api_view(['POST', 'PUT', 'DELETE'])
# def telegram_user(request, format=None):
#     if request.method == "POST":
#         serializer = TelegramUserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == "PUT":
#         serializer = TelegramUserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == "DELETE":
#         try:
#             user = TelegramUser.objects.get(id=request.data['id'])
#             user.delete()
#         except TelegramUser.DoesNotExist:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET'])
# def get_telegram_user(request, id, format=None):
#     if request.method == "GET":
#         if id:
#             try:
#                 user = TelegramUser.objects.get(id=id)
#                 serializer = TelegramUserSerializer(user)
#                 return Response(serializer.data, status=status.HTTP_302_FOUND)
#             except TelegramUser.DoesNotExist:
#                 return Response(status=status.HTTP_204_NO_CONTENT)
#         else:
#             return Response(status=status.HTTP_204_NO_CONTENT)
