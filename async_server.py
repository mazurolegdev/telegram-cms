import asyncio
import os
import ssl
import time
from sqlite3 import OperationalError

import certifi
import requests
from aiohttp import web
from aiohttp.client import ClientSession
from aiojobs.aiohttp import setup, spawn
from apps.telegram.utils import parse_message
from pyrogram import Client

routes = web.RouteTableDef()
loop = asyncio.get_event_loop()
ssl_context = ssl.create_default_context(cafile=certifi.where())

DJANGO_SERVER_URL = os.environ.get('DJANGO_SERVER_URL')
base_link = f'{DJANGO_SERVER_URL}/api/telegram/config/1/012d080a0f9211eab83d0242ac190002012d0b980f9211eab83d0242ac190002/'
link = f'{DJANGO_SERVER_URL}/api/telegram/'
create_message_link = f'{link}message'

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
    response = await session.get(base_link, headers=headers, ssl=ssl_context)
    await session.close()
    return await response.json()


async def get_event_loop():
    try:
        return asyncio.get_event_loop()
    except:
        return asyncio.get_running_loop()


async def get_telegram_app():
    loop = await get_event_loop()
    try:
        return loop.telegram_app
    except:
        await logger('No one loop is running or no one telegram app')
        return None


class Telegram:

    def __init__(self, config=None):
        self.app = None
        self.django_telegram_link = link

        if config:
            self.config = config
            self.django_config_id = self.config['id']
            self.session_name = self.config['session_name']
            self.api_id = self.config['api_id']
            self.api_hash = self.config['api_hash']
            self.access_token = self.config['access_token']
            self.bot_token = self.config['bot_token']
            self.is_bot = self.config['is_bot']
            self.is_active = self.config['is_active']
            self.is_ready = self.config['is_ready']

    async def run_session(self):
        if self.is_ready:
            await self.run()
        else:
            await logger('config is not ready!')

    def send_message(self, to, text):
        self.app.send_message(to, text)
        # await logger(f"sended message [{text}] to [{to}]")

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
                # test_mode=True,
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

        # await self.change_device_model(self.app)
        @self.app.on_message()
        def message_handler(client, message):
            result = parse_message(message)
            result.update({
                "id": self.django_config_id,
                "access_token": self.access_token,
                "app_id": self.api_id,
            })
            requests.post(create_message_link, data=result)

        @self.app.on_disconnect()
        def disconnect_handler(message=None):
            print('disconnect signal')
            print(message)

        self.app.add_handler(message_handler)
        self.app.add_handler(disconnect_handler)
        self.app.start()
        # self.session_string = self.app.export_session_string()
        loop = await get_event_loop()
        loop.telegram_app = self

    async def get_config(self):
        return self.config


@routes.get('/')
async def home(request):
    await spawn(request, logger(request))
    try:
        app = Telegram(await get_configs())
        await app.run_session()
        return web.json_response(await app.get_config())
    except OperationalError:
        return web.json_response({"status": "already running or operational error"})
    except:
        return web.json_response({"status": "unknown error"})


@routes.post('/message/send')
async def get_current_apps(request):
    await spawn(request, logger(request))
    data = await request.post()

    id_to = data['id_to']
    text = data['text']

    app = await get_telegram_app()
    app.send_message(id_to, text)

    return web.json_response({"status": {
        "id_to": id_to,
        "text": text
    }})


@routes.get('/get_updates')
async def get_updates(request):
    await spawn(request, logger(request))
    return web.json_response({"page": "get_updates"})


app = web.Application()
app.add_routes(routes)
setup(app)

if __name__ == '__main__':
    try:
        web.run_app(app)
    except KeyboardInterrupt:
        exit()
