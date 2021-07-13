from speakerapi import serializers
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from medsenger_agent.models import Speaker, Message
from channels.db import database_sync_to_async
import json


class WaitForAuthConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_group_name = None
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
                await database_sync_to_async(Speaker.objects.get)(
                    token=token)
            except Speaker.DoesNotExist:
                await self.send("Invalid token")
                await self.close()
                return

            s = await database_sync_to_async(
                Speaker.objects.select_related('contract').get)(
                    token=token)

            if s.contract is not None:
                await self.send('OK')
                await self.close()
            else:
                self.room_group_name = 'auth_%s' % s.id
                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )
            return

        await self.send(json.dumps(serializer.errors, ensure_ascii=False))
        await self.close()

    async def receive_authed(self, event):
        await self.send('OK')
        await self.close()

    def get_serializer(self, *, data):
        return serializers.CheckAuthSerializer(data=data)


class IncomingMessageNotifyConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_group_name = None
        await self.accept()

    async def disconnect(self, close_code):
        if self.room_group_name is not None:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def process_first_input(self, content, **kwargs):
        message = None
        try:
            m = await database_sync_to_async(
                Message.objects.filter)(
                    contract=kwargs['s'].contract, is_notified=False)
            message = await database_sync_to_async(
                m.earliest)('date')
        except Message.DoesNotExist:
            pass

        if message is not None:
            data = {
                'text': message.text,
                'id': message.id
            }

            await self.send(json.dumps(data, ensure_ascii=False))

        self.room_group_name = 'message_%s' % kwargs['s'].contract.contract_id
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

    async def make_message_notified(self, content, **kwargs):
        if 'message_id' not in content:
            self.send_json({"message_id": ["field required"]})
            self.close()
            return

        try:
            m = await database_sync_to_async(Message.objects.get)(
                id=content['message_id'])
        except Message.DoesNotExist:
            self.send_json(["Message does not exists with given id"])
            self.close()
            return

        m.is_notified = True
        await database_sync_to_async(m.save)()

    async def make_message_red(self, content, **kwargs):
        if 'message_id' not in content:
            self.send_json({"message_id": ["field required"]})
            self.close()
            return

        try:
            m = await database_sync_to_async(Message.objects.get)(
                id=content['message_id'])
        except Message.DoesNotExist:
            self.send_json(["Message does not exists with given id"])
            self.close()
            return

        m.is_red = True
        await database_sync_to_async(m.save)()

    async def receive_json(self, content, **kwargs):
        serializer = serializers.IncomingMessageNotify(data=content)
        if serializer.is_valid():
            token = serializer.data['token']

            try:
                s = await database_sync_to_async(
                    Speaker.objects.select_related('contract').get)(
                        token=token)
                kwargs['s'] = s
            except Speaker.DoesNotExist:
                await self.send("Invalid token")
                await self.close()
                return

            if 'notified_message' in serializer.data:
                return await self.make_message_notified(
                    serializer.data, **kwargs)
            elif 'red_message' in serializer.data:
                return await self.make_message_red(serializer.data, **kwargs)
            else:
                return await self.process_first_input(
                    serializer.data, **kwargs)

        await self.send(json.dumps(serializer.errors, ensure_ascii=False))
        await self.close()

    async def receive_message(self, event):
        await self.send(json.dumps({
                "text": event['message'],
                "id": event['message_id']
            }, ensure_ascii=False))
