import requests
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError

from apps.telegram.models import Config, Scene
from apps.telegram.utils import telegram_logger
from main.celery import app


class TriggerMiddlewareTasks:

    @staticmethod
    def get_app(data):
        if data['is_bot_session'] == 'True':
            return Config.objects.get(api_id=data['app_id'], is_bot=True)

        elif data['is_bot_session'] == 'False':
            return Config.objects.get(api_id=data['app_id'], is_bot=False)

    @staticmethod
    @app.task()
    def private_pre_task(data):
        app = TriggerMiddlewareTasks.get_app(data)
        scenes = Scene.objects.filter(app=app, is_enabled=True)

        triggers = []
        for scene in scenes:
            triggers.append(scene.triggers.all())

        # FIXME
        current_trigger_instance = None

        for trigger in triggers[0]:
            if trigger.is_enabled and trigger.middleware_type:
                try:
                    trigger.get_reason().start(
                        trigger, data, app, current_trigger_instance
                    )

                except MultiValueDictKeyError:
                    telegram_logger(f"Catch MultiValueDictKeyError at private_pre_task. Data {data}")

    @staticmethod
    @app.task()
    def private_post_task():
        pass


@app.task()
def start_bots_crawling():
    response = requests.get(settings.ASYNC_SERVER_URL)
    print(response)


@app.task()
def send_telegram_message(model):
    model.send_message()
    return None
