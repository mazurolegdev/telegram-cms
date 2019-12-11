import asyncio
import ssl
import time
import json

import certifi
import requests
from aiohttp import web
from aiohttp.client import ClientSession
from aiojobs.aiohttp import setup, spawn
from pyrogram import Client

from apps.telegram.utils import parse_message
from main.settings import DJANGO_SERVER_URL

routes = web.RouteTableDef()
loop = asyncio.get_event_loop()
ssl_context = ssl.create_default_context(cafile=certifi.where())

GET_CONFIG_LIST = f'{DJANGO_SERVER_URL}/api/telegram/config/all/'
link = f'{DJANGO_SERVER_URL}/api/telegram/'
create_message_link = f'{link}message'
create_group_url = f"{DJANGO_SERVER_URL}/api/telegram/group"

headers = {
    "content-type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
}


async def logger(message):
    print(f"[{time.ctime()}]: {message}")


async def gen_session():
    session = ClientSession(loop=loop)
    return session


async def get_configs():
    session = await gen_session()
    response = await session.get(GET_CONFIG_LIST, headers=headers, ssl=ssl_context)
    await session.close()
    return await response.json()


async def get_event_loop():
    try:
        return asyncio.get_event_loop()
    except:
        return asyncio.get_running_loop()


class TelegramAppConnector:
    def __init__(self, data=None):
        self.connectors = []
        self.default_connector = None
        if data:
            self.telegram_instance = data['telegram_instance']
            self.app = data['app']
            self.app_id = data['app_id']
            self.api_hash = data['api_hash']
            self.session_name = data['session_name']
            self.session_string = data['session_string']
            self.is_bot_session = data['is_bot_session']
            self.is_ready = data['is_ready']
            self.is_active = data['is_active']
            self.connected = data['connected']

    def add(self, connector, default=None):
        assert isinstance(connector, TelegramAppConnector)
        self.connectors.append(connector)

        if default:
            self.default_connector = connector

    def get_default_connector(self):
        return self.default_connector

    def get(self, data):
        is_bot_session = bool(data['is_bot_session'])
        app_id = int(data['app_id'])
        session_name = str(data['session_name'])
        session_string = str(data['session_string'])

        for connector in self.connectors:
            if str(connector.session_string) == session_string and bool(connector.is_bot_session) == is_bot_session:
                return connector


connector = TelegramAppConnector()


class Telegram:

    def __init__(self, config=None):
        self.app = None
        self.django_telegram_link = link
        self.init_apps = []
        self.connector = None
        self.session_string = None
        self.groups = []

        if config:
            self.config = config
            self.django_config_id = self.config['id']
            self.session_name = self.config['session_name']
            self.api_id = self.config['api_id']
            self.api_hash = self.config['api_hash']
            self.access_token = self.config['access_token']
            self.bot_token = self.config['bot_token']
            self.is_bot = bool(self.config['is_bot'])
            self.is_active = bool(self.config['is_active'])
            self.is_ready = bool(self.config['is_ready'])

    async def run_session(self):
        if self.is_ready:
            await self.run()
        else:
            await logger('config is not ready!')

    def get_updates_groups(self):
        for line in self.app.get_dialogs():
            if line['chat']['type'] != 'private' and line['chat']['type'] != 'bot':
                if not line['chat'] in self.groups:
                    chat = line['chat']
                    permissions = chat['permissions']
                    data = {
                        "id": str(chat['id']),
                        "type": str(chat['type']),
                        "is_verified": bool(chat['is_verified']),
                        "is_restricted": bool(chat['is_restricted']),
                        "is_scam": bool(chat['is_scam']),
                        "title": str(chat['title']),
                        "username": str(chat['username']),
                        # "can_send_messages": bool(permissions['can_send_messages']),
                        # "can_send_media_messages": bool(permissions['can_send_media_messages']),
                        # "can_send_other_messages": bool(permissions['can_send_other_messages']),
                        # "can_add_web_page_previews": bool(permissions['can_add_web_page_previews']),
                        # "can_send_polls": bool(permissions['can_send_polls']),
                        # "can_change_info": bool(permissions['can_change_info']),
                        # "can_invite_users": bool(permissions['can_invite_users']),
                        # "can_pin_messages": bool(permissions['can_pin_messages']),
                    }
                    self.groups.append(data)
        return self.groups

    def get_groups(self):
        return self.groups

    def send_message(self, to, text):
        self.app.send_message(to, text)

    async def run(self):
        if self.is_bot:
            await logger('Init Bot session')
            self.app = Client(
                self.session_name,
                api_id=self.api_id,
                api_hash=self.api_hash,
                bot_token=self.bot_token,
                workers=2,
                workdir='apps/telegram/sessions/',
                device_model='MacBookPro12,1, macOS 10.14.6',
                app_version='Telegram macOS 5.8 (185085) APPSTORE',
                system_version='Darwin 18.7.0',
            )

        if not self.is_bot:
            await logger('Init User-Bot session')
            self.app = Client(
                self.session_name,
                api_id=self.api_id,
                api_hash=self.api_hash,
                workers=2,
                workdir='apps/telegram/sessions/',
                device_model='MacBookPro12,1, macOS 10.14.6',
                app_version='Telegram macOS 5.8 (185085) APPSTORE',
                system_version='Darwin 18.7.0',
            )

        @self.app.on_message()
        def message_handler(client, message):
            result = parse_message(message)
            result.update({
                "id": self.django_config_id,
                "access_token": self.access_token,
                "app_id": self.api_id,
                "api_hash": self.api_hash,
                "session_name": self.session_name,
                "is_bot_session": self.is_bot,
            })
            requests.post(create_message_link, data=result)

        @self.app.on_disconnect()
        def disconnect_handler(message=None):
            print('disconnect signal')
            print(message)

        self.app.add_handler(message_handler)
        self.app.add_handler(disconnect_handler)
        self.app.start()

        self.session_string = self.app.export_session_string()

        app_data = {
            "app_id": self.api_id,
            "api_hash": self.api_hash,
            "session_name": self.session_name,
            "session_string": self.session_string,
            "access_token": self.access_token,
            "is_bot_session": self.is_bot,
            "is_ready": self.is_ready,
            "is_active": self.is_active,
            "connected": self.app.is_connected,
        }

        requests.post(f'{DJANGO_SERVER_URL}/api/telegram/config', data=app_data)

        app_data.update({
            "telegram_instance": self,
            "app": self.app,
        })
        self.connector = TelegramAppConnector(app_data)

        if not self.is_bot:
            connector.add(self.connector, default=True)
        else:
            connector.add(self.connector)

    async def get_config(self):
        return self.config


async def fetch(configs):
    for config in configs:
        app = Telegram(config)
        await app.run_session()


@routes.get('/')
async def home(request):
    await spawn(request, logger(request))
    try:
        configs = await get_configs()

        await fetch(configs)
        return web.json_response({"configs": configs})
    except:
        return web.json_response({"status": "already running or operational error"})

@routes.post('/get_groups')
async def get_groups(request):
    await spawn(request, logger(request))

    data = await request.post()
    connection = connector.get(data)

    if not connection:
        connection = connector.get_default_connector()

    return web.json_response(connection.telegram_instance.get_updates_groups())


@routes.post('/message/send')
async def send_message(request):
    await spawn(request, logger(request))

    data = await request.post()
    connection = connector.get(data)

    if not connection:
        connection = connector.get_default_connector()

    id_to = data['id_to']
    text = data['text']

    connection.app.send_message(id_to, text)
    return web.json_response({"page": "get_connector"})


app = web.Application()
app.add_routes(routes)
setup(app)

if __name__ == '__main__':
    try:
        web.run_app(app)
    except KeyboardInterrupt:
        exit()
