import asyncio
import os
import subprocess

loop = asyncio.get_event_loop()


async def main():
    # do something
    pass


async def log(message):
    print(message)


async def entrypoint():
    await log('-------------------------')
    await log('This is entrypoint for python3.')
    await log('You can use ane commands you want inside python3 runtime before docker image starts')
    await log('-------------------------')

    os.environ.setdefault("SECRET_KEY", "pd9g8r&z=&o4o1h#_*=bi826_=fu#@zq8le1553cpjq6cs&sw6")
    os.environ.setdefault("ASYNC_SERVER_URL", "http://172.25.0.3:8080")
    os.environ.setdefault("DJANGO_SERVER_URL", "http://172.25.0.2:8005")
    # os.environ.setdefault("TELEGRAM_SESSION_NAME", "netcraft_session")
    # os.environ.setdefault("TELEGRAM_API_ID", "1116803")
    # os.environ.setdefault("TELEGRAM_API_HASH", "28087f6ca9723f3d1369f8de5f9a5979")


    print("Entrypoint is done!")

    await main()


if __name__ == '__main__':
    loop.run_until_complete(entrypoint())
