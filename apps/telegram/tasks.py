import requests
from apps.telegram.models import Config, BaseScene
from apps.telegram.utils import telegram_logger, get_triggers_from_scene
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError
from main.celery import app


class TriggerMiddlewareTasks:

    @staticmethod
    @app.task()
    def private_pre_task(data):

        app = Config.objects.get(api_id=data['app_id'])
        scenes = BaseScene.objects.filter(app=app, is_enabled=True)
        print(f"scenes: {scenes}")
        triggers = [get_triggers_from_scene(scene) for scene in scenes]
        print(f"triggers: {triggers}")

        for trigger in triggers:
            if trigger[0].is_enabled and trigger[0].middleware_type:
                try:
                    trigger[0].get_reason().start(
                        trigger[0], data
                    )

                except MultiValueDictKeyError:
                    telegram_logger(f"Catch MultiValueDictKeyError at private_pre_task. Data {data}")

    @staticmethod
    @app.task()
    def private_post_task():
        print('Init post task')


@app.task()
def start_bots_crawling():
    response = requests.get(settings.ASYNC_SERVER_URL)
    print(response)


@app.task()
def send_telegram_message(model):
    model.send_message()
    return None
