# Telegram-CMS v.0.3. alpha
- Based on Opencluster https://opencluster-hub.github.io/opencluster/


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

# This build is for local demonstration or for UNSAFE local usind only!
For production using, you need change database!

# Before start use Telegram CMS, > Entry with telegram API:
- sh ./create_session.sh
- go for instructions inside bash script [will be fixed for creating session inside django admin panel]
- added same config inside django admin panel at Configs application [will be fixed for full automatization]

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

Developing by me for people with love <3
