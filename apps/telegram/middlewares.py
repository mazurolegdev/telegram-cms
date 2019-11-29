from rest_framework import status
from rest_framework.response import Response
from django.utils.datastructures import MultiValueDictKeyError

class TriggerMiddleware:
    def __init__(self, middleware_model=None):
        from apps.telegram.utils import telegram_logger
        from apps.telegram.tasks import TriggerMiddlewareTasks

        self.model = middleware_model
        self.triggers = None
        self.trigger = None
        self.app = None
        self.text = None
        self.logger = telegram_logger
        self.task = TriggerMiddlewareTasks()


    def message(self, func):
        def wrapper(request, *args, **kwargs):

            if request.data['chat_type'] == 'private':
                self.logger(f"Catch non private message", self)

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
