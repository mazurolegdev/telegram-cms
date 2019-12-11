import requests
import json
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError

from apps.telegram.models import Config, Scene, ChatListener, Chat
from apps.telegram.utils import telegram_logger, DataCleaner, Sender
from main.celery import app


class Group:

    @staticmethod
    def create_group(data):
        '''
        {'id': '-1001294234578',
        'type': 'supergroup', # or 'channel'
        'is_verified': 'False',
        'is_restricted': 'False',
        'is_scam': 'False',
        'title': 'Some cool public',
        'username': 'gtgtgththt',
        '''
        try:
            chat = Chat.objects.get(
                tg_chat_id=int(data['id']),
                tg_chat_type=str(data['type']),
                tg_chat_title=str(data['title']),
                tg_chat_username=str(data['username'])
            )
        except Chat.DoesNotExist:
            chat = Chat.objects.create(
                tg_chat_id=int(data['id']),
                tg_chat_type=str(data['type']),
                tg_chat_title=str(data['title']),
                tg_chat_username=str(data['username'])
            )
        print(chat)


    @staticmethod
    @app.task()
    def get_groups(app_id: int):
        '''
        {'is_bot_session': False,
        'app_id': 1116803,
        'session_name': 'netcraft_session',
        'session_string': 'AgBpeooUViRREXOS0BNRtcAPLpNLc7cuv2f29DjSbfXYFLs6zDIZRUJCcJi5V5KAux\
        AfzMwsbXWdcM4dROdztHTzxOrVcR8AMg8lLZLnNzfvhEy5iAXvlZFxzJJo9YnIchllud'}
        '''
        app = Config.objects.get(id=app_id)
        groups = Sender.get_groups(app)

        for group in json.loads(groups):
            Group.create_group(group)


class ChatListenerTasks:
    @staticmethod
    @app.task()
    def default_chat_listener_task(data):
        try:
            chat_id = data['chat_id']
            chat_username = data['chat_username']
            chat_type = data['chat_type']
            text = data['text']
        except MultiValueDictKeyError:
            telegram_logger(f"MultiValueDictKeyError at data: {data}", 'ChatListenerTasks')
            return 1

        listeners = ChatListener.objects.filter(is_enabled=True)

        for listener in listeners:
            if listener.auto_publishing_is_enabled:
                if str(chat_id) == str(listener.from_chat.tg_chat_id):
                    response_data = DataCleaner.clean_response_chat_data(data, listener)
                    response_data.update({"text": data['text']})
                    Sender.send_message(response_data)


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

        if triggers:
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
