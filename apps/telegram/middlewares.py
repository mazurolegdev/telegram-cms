from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.response import Response
from apps.telegram.models import ChatListener, Config
from apps.telegram.utils import telegram_logger, Sender, DataCleaner
from apps.telegram.api.serializers import ConfigSerializer
from apps.telegram.tasks import TriggerMiddlewareTasks, ChatListenerTasks


class RequestsMiddleware:
    def __init__(self):
        self.logger = telegram_logger

    def post(self, func):
        def wrapper(request, *args, **kwargs):
            if request.method == "POST":
                return func(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        return wrapper


class ApplicationMiddleware:
    def __init__(self):
        self.logger = telegram_logger

    def update(self, func):
        def wrapper(request, *args, **kwargs):
            app_id = request.data['app_id']
            api_hash = request.data['api_hash']
            session_name = request.data['session_name']
            access_token = request.data['access_token']
            session_string = request.data['session_string']
            is_bot_session = request.data['is_bot_session']

            try:
                app = Config.objects.get(
                    session_name=session_name,
                    api_id=app_id,
                    api_hash=api_hash,
                    is_bot=is_bot_session,
                )
                if str(access_token) == str(app.access_token):
                    app.session_string = session_string
                    app.save()

                    serializer = ConfigSerializer(app)
                    return Response(serializer.data, status=status.HTTP_200_OK)

                else:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)

            except Config.DoesNotExist:
                return Response(status=status.HTTP_204_NO_CONTENT)

        return wrapper


class TriggerMiddleware:
    def __init__(self):
        self.logger = telegram_logger
        self.task = TriggerMiddlewareTasks()

    def message(self, func):
        def wrapper(request, *args, **kwargs):

            if request.data['chat_type'] == 'private':
                self.logger(f"Catch private message", self)

                try:
                    self.task.private_pre_task.delay(request.data)

                    # here you can do what ever you want

                    self.task.private_post_task.delay()
                    return func(request, *args, **kwargs)

                except MultiValueDictKeyError:
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            else:
                self.logger(f"Catch non private message", self)
                return func(request, *args, **kwargs)

        return wrapper


class ListenerMiddleware:
    def __init__(self):
        self.logger = telegram_logger
        self.task = ChatListenerTasks()

    def chat(self, func):
        def wrapper(request, *args, **kwargs):
            if request.data['chat_type'] != 'private':
                self.task.default_chat_listener_task(request.data)
            return func(request, *args, **kwargs)

        return wrapper
