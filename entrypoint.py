import asyncio
import os

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
    # os.environ.setdefault("REDIS_CHANNELS_LAYER_HOST", [('redis', 6379)])
    os.environ.setdefault("ASYNC_SERVER_URL", "http://172.25.0.3:8080")
    os.environ.setdefault("DJANGO_SERVER_URL", "http://172.25.0.2:8005")

    await main()


if __name__ == '__main__':
    loop.run_until_complete(entrypoint())
