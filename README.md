# Telegram-CMS v.0.3. alpha
- Based on Opencluster https://opencluster-hub.github.io/opencluster/

![img](http://dl3.joxi.net/drive/2019/12/06/0029/3762/1904306/06/08fa2e0135.jpg)

Instruments:
- Docker
- Django framework
- Django Rest Framework
- Aiohttp + Aiojobs
- Pyrogram
- Celery
- Redis
- Swagger
- Redoc

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
# Containers connected with network inside docker

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

# Default Trigger Middleware Usage:
Check for your app is fully connected to telegram api. Create post.view with django rest framework. import middleware decorator this way - from apps.telegram.middlewares import TriggerMiddleware, and init it like this - trigger = TriggerMiddleware(), then add to your post.view this way decorator:


- @api_view(['POST'])
- @trigger.message
- def create_message(request):
-   ...

Now, you should create Base scene in django admin panel and add some triggers with triggered words and answers.
Now its completly done for catch triggers messages with words and answers you want!
Now its works only for private messages!

# Expectation in v.0.4. alpha:
- Finish state mahine for scenes and triggers.
- Adding new default triggers!
- Customize CMS API for handle AI recognition patterns

Developing by me for people with love <3

