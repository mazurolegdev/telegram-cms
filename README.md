# Telegram-CMS v.0.3.2 alpha
- Based on Opencluster https://opencluster-hub.github.io/opencluster/

![img](http://dl3.joxi.net/drive/2019/12/06/0029/3762/1904306/06/08fa2e0135.jpg)

Instruments:
- [Docker](https://www.docker.com/)
- [Django framework](https://www.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [Django Channels](https://channels.readthedocs.io/en/latest/)
- [Aiohttp](https://aiohttp.readthedocs.io/en/stable/) + [Aiojobs](https://aiojobs.readthedocs.io/en/stable/quickstart.html)
- [Pyrogram](https://docs.pyrogram.org/)
- [Celery](http://www.celeryproject.org/)
- [Redis](https://redis.io/)
- [Swagger](https://swagger.io/)
- [Redoc](https://github.com/Redocly/redoc)

# Short feature list:
- It works with bot's and user's accounts
- It can parse all account groups and channels
- It can parse all account contacts and dialogs
- It can talk with users using Triggers System
- It can broadcast any posts of any channels and groups to your channel or your contact. Even if you are not a admin of parsed group.
- It can broadcast content from any groups and channels to any groups and channels with Group Listeners. Even if you are not a admin of parsed group. [need fix]
- It can broadcast content from RSS Feeds to any groups and channels with RSS Listeners. Even if you are not a admin of parsed group. [need fix]
- It can schedule content to any groups and channels. Even if you are not a admin of parsed group. [need fix]
- It got handle API for 90% of features. [not started yet]
- It can handle API for Text Recognitions. [not started yet]
- It can make visit statistics for any groups and channels you want. [not started yet]
- It can make sales statistics. [not started yet]

# Short architecture description:
- State machine inside Django's MVC and Aiohttp. Both got API.

- Pyrogram inside aiohttp with accounts connectors and easy api.
- Pyrogram listen all account updates and send it to Django.
- Custom Django middlewares catch request data from aiohttp, and send it to handle tasks.
- Tasks make business logic and send result to Aiohttp > Account connector > Pyrogram > Telegram API.
- Most of code inside Aiohttp is asynchronous.

# Docker containers:
- Django
- Aiohttp
- Celery
- Redis
- Memcached
- Nginx
# Containers connected with bridge inside docker

# Setup:
- Install Docker and docker-compose
- git clone https://github.com/codefather-labs/telegram-cms.git
- touch .env
- start docker daemon if it not started
- docker-compose build
- docker-compose up
- http://0.0.0.0:80/admin
- login: admin
- password: admin

# This build is for demonstration or for UNSAFE local using only!
For production using, you need change database!

# Before start use Telegram CMS, > Entry with telegram API:
- sh ./create_session.sh
- go for instructions inside bash script [will be fixed for creating session inside django admin panel]
- added same config inside django admin panel at Configs application [will be fixed for full automatization]

# Getting started with Telegram CMS
- create session with same options as create_session.sh file

![img](http://dl4.joxi.net/drive/2019/12/06/0029/3762/1904306/06/7e6fe98225.jpg)

- create some dialog scene

![img](http://dl3.joxi.net/drive/2019/12/06/0029/3762/1904306/06/2feeeee9ec.jpg)

- create triggers chain
- Warn! Use entrypoint value at started trigger dialog and exitpoint value at exit trigger dialog

![img](http://dl4.joxi.net/drive/2019/12/06/0029/3762/1904306/06/f2f7cabdfc.jpg)

- Customize your triggers chain!

![img](http://dl3.joxi.net/drive/2019/12/06/0029/3762/1904306/06/8b1a7a4c8e.jpg)
![img](http://dl3.joxi.net/drive/2019/12/06/0029/3762/1904306/06/ec1691248c.jpg)

- Next trigger

![img](http://dl4.joxi.net/drive/2019/12/06/0029/3762/1904306/06/34f25442f7.jpg)
![img](http://dl4.joxi.net/drive/2019/12/06/0029/3762/1904306/06/ed1ec9fc5f.jpg)

- And last trigger (except one). Exitpoint instance!

![img](http://dl4.joxi.net/drive/2019/12/06/0029/3762/1904306/06/5c53af1960.jpg)
![img](http://dl4.joxi.net/drive/2019/12/06/0029/3762/1904306/06/e4295a8a3c.jpg)

# v.0.2. alpha Features and notes:
- added default Trigger middleware [auto answered middlewares with usable triggers system inside django admin panel]

# v.0.3 alpha Features and notes
- updates for default Trigger middlewares [more awesome features]
- added Scenes (Scene of dialog) - now admin of django need to create Scene of dialog with user inside django admin panel. Just like need it at CMS!
- starts added state machine for Scenes
- added mode states for triggers [is_reverse_trigger, is_action, and other]
- fixed Telegram API connectors on Aiohttp. Its fully work as multi-account system
- added telegram plugin to django-admin-panel for session usage
- and more other awesome things!

# Listener Middleware Usage:
Check for your app is fully connected to telegram api. Create post.view with django rest framework, and go this way:
- from apps.telegram.middlewares import ListenerMiddleware
- listener = ListenerMiddleware()

- @api_view(['POST'])
- @listener.message
- def create_message(request):
-   ...

Now, all of incoming messages will be handle with ListenerMiddlware, wich got default functions for all kinds of messages. You should create Base scene in django admin panel and add some triggers with triggered words and answers, for Trigger Middleware handle private messages. Add groups listeners for Listener Middleware handle non private messages.

# Expectation in v.0.4. alpha:
- Finish state mahine for scenes and triggers. +
- Adding new default triggers! +
- Customize CMS API for handle AI recognition patterns ?

Developing by me for people with love <3

