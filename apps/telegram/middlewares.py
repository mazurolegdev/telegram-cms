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


    def middleware(self, func):
        def wrapper(request, *args, **kwargs):
            from apps.telegram.models import Trigger, Config

            try:
                self.app_id = request.data['app_id']
                self.text = request.data['text']
                self.sender_id = request.data['sender_id']
                self.sender_username = request.data['sender_username']

                if request.data['chat_type'] == 'private':
                    pass

                self.app = Config.objects.get(api_id=self.app_id)

                self.triggers = Trigger.objects.filter(app=self.app)
                self.pre_task()

                # here you can do what ever you want

                self.post_task()
                return func(request, *args, **kwargs)

            except Config.DoesNotExist:
                return Response(status=status.HTTP_204_NO_CONTENT)

            except Trigger.DoesNotExist:
                return Response(status=status.HTTP_204_NO_CONTENT)

            except MultiValueDictKeyError:
                print(request.data)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # except:
            #     return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return wrapper

    def pre_task(self):
        for trigger in self.triggers.all():
            self.task.pre_task.delay(
                str(self.app.id),
                str(trigger.id),
                str(self.sender_id),
                str(self.sender_username),
                str(self.text)
            )


    def post_task(self):
        self.task.post_task.delay()
