import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from medsenger_agent.models import Speaker
from staff import serializers


class IssuesConsumer(AsyncJsonWebsocketConsumer):
    room_group_name = None

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        if self.room_group_name is not None:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive_json(self, content, **kwargs):
        serializer = self.get_serializer(data=content)
        if serializer.is_valid():
            token = serializer.data['token']

            try:
                s = await database_sync_to_async(Speaker.objects.get)(token=token)
            except Speaker.DoesNotExist:
                await self.send("Invalid token")
                await self.close()
                return

            self.room_group_name = 'speaker_issue_%s' % s.pk
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            return

        await self.send(json.dumps(serializer.errors, ensure_ascii=False))
        await self.close()

    async def receive_issue(self, event):
        await self.send(json.dumps(event['data'], ensure_ascii=False))

    @staticmethod
    def get_serializer(*args, **kwargs):
        return serializers.InitSpeakerSerializer(*args, **kwargs)
