import asyncio
# from utils import log

from pyrogram import Client
from pyrogram.errors import BadRequest, Forbidden, PhoneNumberBanned, UserBannedInChannel


loop = asyncio.get_event_loop()





def change_device_model(app, model):
    app.DEVICE_MODEL = model

def create_session_from_command_line():
    print('Чтобу получить API доступ к вашему аккаунту и создать сессию,'
          'Нужно перейти по ссылке https://my.telegram.org/ и авторизоваться.'
          'Далее создать приложение с любым названием и любой платформой.'
          'Как правило название это набор рандомных символов. Это нормально.'
          'Далее вы получите API_ID и API_HASH. Их нужно будет вставить по инструкции ниже,'
          'чтобы инициализировать сессию вашего телеграм аккаунта.')
    api_id = input("Введите API_ID:")
    api_hash = input("Введите API_HASH:")
    session_name = input("Введите название сессии (только латинница):")

    app = Client(
        session_name,
        api_id,
        api_hash,
        workdir='apps/telegram/sessions/',
        device_model='MacBookPro13,1, macOS 10.14.6',
        app_version='Telegram macOS 5.8 (185085) APPSTORE',
        system_version='Darwin 18.7.0',
    )
    try:
        app.start()
        app.stop()
        print(f"Сессия успешно создана. Теперь она находится в папке apps/telegram/sessions "
              f"и будет использоваться в дальнейшем для коммуникации с телеграм API."
              f"API_ID: {api_id}."
              f"API_HASH: {api_hash}"
              f"SESSION_NAME: {session_name}")
    except:
        print("Не удалось создать сессию. Что-то пошло не так. :(")


async def create_session():
    app = Client(
        'netcraft_session',
        api_id=1116803,
        api_hash='28087f6ca9723f3d1369f8de5f9a5979',
        workdir='sessions/',
        device_model='MacBookPro12,1, macOS 10.14.6',
        app_version='Telegram macOS 5.8 (185085) APPSTORE',
        system_version='Darwin 18.7.0',
        # test_mode=True,
    )
    app.start()
    app.stop()

async def main(config, session):
    from apps.telegram.utils import log, parse_message
    session = config['session_name']
    api_id = config['api_id']
    api_hash = config['api_hash']
    bot_token = config['bot_token']

    if config['is_bot']:
        log('Init Bot session', 1)
        app = Client(
            'my_bot',
            api_id=api_id,
            api_hash=api_hash,
            bot_token=bot_token,
            workdir='sessions/',
            test_mode=True
        )

    if not config['is_bot']:
        log('Init User-Bot session', 1)
        app = Client(
            api_id=api_id,
            api_hash=api_hash,
            # bot_token=bot_token,
            workdir='sessions/',
            test_mode=True,
        )

    change_device_model(app, model='Macbook Pro 13 Retina')

    app.start()

    @app.on_message()
    def message_handler(client, message):
        result = parse_message(message)

    @app.on_disconnect()
    def disconnect_handler(message=None):
        print('disconnect signal')
        print(message)

    app.add_handler(message_handler)
    app.add_handler(disconnect_handler)

    log(f'Device model: {app.DEVICE_MODEL}', 1)
    # await send_message(app, 'me', 'hey!!!')
    # app.idle()


if __name__ == '__main__':
    try:
        create_session_from_command_line()
    except KeyboardInterrupt:
        pass
