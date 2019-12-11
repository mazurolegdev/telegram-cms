from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.common.secret_note.models import Note
from apps.common.secret_note.api.serializers import NoteSerializer

from apps.telegram.middlewares import ListenerMiddleware
from apps.telegram.models import Trigger

listener = ListenerMiddleware()


@api_view(['GET'])
def get_note(request, id, access_token):
    if request.method == 'GET':
        try:
            note = Note.objects.get(id=id)
            if str(access_token) == str(note.access_token):
                note.pre_delete()
                serializer = NoteSerializer(note)
                data = serializer.data
                note.delete()
                return Response(data, status=status.HTTP_200_OK)

            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        except Note.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@listener.message
def test_middleware(request):
    if request.method == "POST":
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_note(request):
    if request.method == 'POST':
        if request.data['text']:
            try:
                new_note = Note.objects.create(
                    text=request.data['text']
                )
                serializer = NoteSerializer(new_note)
                return Response(serializer.data, status=status.HTTP_200_OK)

            except AttributeError:
                return Response({
                    "status": "error",
                    "about": "attribute error"
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "status": "error",
                "about": "cant found text"
            }, status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)