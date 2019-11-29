# Telegram-CMS v.0.2. alpha
- Based on Opencluster https://opencluster-hub.github.io/opencluster/


# Setup:
- Install Docker and docker-compose
- git clone https://github.com/codefather-labs/telegram-cms.git
- docker-compose build
- docker-compose up

# Entry with telegram API:
- sh ./create_session.sh
- go for instructions inside bash script [will be fixed for creating session inside django admin panel]
- added same config inside django admin panel at Configs application [will be fixed for full automatization]

# v.0.2. alpha Features and notes:
- added default Trigger middleware [auto answered middlewares with usable triggers system inside django admin panel]

# Default Trigger Middleware Usage:
Check for your app is fully connected to telegram api. Create post.view with django rest framework. import middleware decorator this way - from apps.telegram.middlewares import TriggerMiddleware, and init it like this - trigger = TriggerMiddleware(), then add to your post.view this way decorator:


- @api_view(['POST'])
- @trigger.message
- def create_message(request):
-   ...

Now, you should create Base scene in django admin panel and add some triggers with triggered words and answers.
Now its completly done for catch triggers messages with words and answers you want!
Now its works only for private messages!

# Expectation in v.0.3. alpha:
- creating sessions inside django admin panel
- auto adding config from session
- more things for default Trigger middleware

Developing by me for people with love <3
