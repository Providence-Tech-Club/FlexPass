import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer


class RequestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logging.warn("connect")
        self.user_id = self.scope["user"].id
        logging.warn(self.user_id)
        self.group_name = f"user_updates_{self.user_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        logging.warn("disconnect")
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def status_update(self, event):
        logging.warn("status_update")
        await self.send(
            text_data=json.dumps(
                {"message": event["message"], "status": event["status"]}
            )
        )
