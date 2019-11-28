import asyncio
import json
from channels.consumer import AsyncConsumer
from apps.core.models import Account

from django.conf import settings


class AccountConsumer(AsyncConsumer):

    async def websocket_connect(self, message):
        scope = self.scope
        try:
            account = Account.objects.get(
                user=scope['user'],
            )
        except:
            account = Account.objects.create(
                user=scope['user'],
            )
        account.online = True
        account.save()

        await self.send({
            "type": "websocket.accept",
        })

        await self.send({
            "type": "websocket.send",
            "text": json.dumps({"account": {
                "user_id": account.user.id,
                "username": account.user.username,
                "email": account.user.email,
                "online": account.online
            }}),
        })

    async def websocket_disconnect(self, message):
        scope = self.scope
        account = Account.objects.get(
            user=scope['user'],
        )
        account.online = False
        account.save()
        await self.send({
            "type": "websocket.disconnect",
            "text": "disconnected"
        })
        # await self.send({
        #     "type": "websocket.send",
        #     "text": json.dumps({
        #         "status": "disconnected"
        #     })
        # })

    async def websocket_receive(self, message):
        await asyncio.sleep(1)
        await self.send({
            "type": "websocket.send",
            "text": f"{message}",
        })
