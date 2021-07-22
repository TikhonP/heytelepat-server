import json
import medsenger_api

from django.conf import settings

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from medsenger_agent.models import (
    Speaker,
    Message,
    MeasurementTask,
    MedicineTaskGeneric,
)
from speakerapi import serializers
from medsenger_agent import serializers as ma_serializers

aac = medsenger_api.AgentApiClient(settings.APP_KEY)


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

    async def receive_authed(self, _):
        await self.send('OK')
        await self.close()

    @staticmethod
    def get_serializer(*args, **kwargs):
        return serializers.CheckFirmwareSerializer(*args, **kwargs)


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
            data = serializers.MessageSerializer(message).data
            await self.send(json.dumps(data, ensure_ascii=False))

        self.room_group_name = 'message_%s' % kwargs['s'].contract.contract_id
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

    async def make_message_notified(self, content, **kwargs):
        if 'message_id' not in content:
            await self.send_json({"message_id": ["field required"]})
            await self.close()
            return

        try:
            m = await database_sync_to_async(Message.objects.get)(
                id=content['message_id'])
        except Message.DoesNotExist:
            await self.send_json(["Message does not exists with given id"])
            await self.close()
            return

        m.is_notified = True
        await database_sync_to_async(m.save)()

    async def make_message_red(self, content, **kwargs):
        if 'message_id' not in content:
            await self.send_json({"message_id": ["field required"]})
            await self.close()
            return

        try:
            m = await database_sync_to_async(Message.objects.get)(
                id=content['message_id'])
        except Message.DoesNotExist:
            await self.send_json(["Message does not exists with given id"])
            await self.close()
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
        await self.send(json.dumps(event['data'], ensure_ascii=False))


class MeasurementNotifyConsumer(AsyncJsonWebsocketConsumer):
    serializer = serializers.IncomingMeasurementNotify
    out_serializer = ma_serializers.TaskModelSerializer

    async def connect(self):
        self.room_group_name = None
        await self.accept()

    async def disconnect(self, close_code):
        if self.room_group_name is not None:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def first_init(self, content, **kwargs):
        measurement = None
        try:
            m = await database_sync_to_async(
                MeasurementTask.objects.filter)(
                contract=kwargs['s'].contract, is_sent=False)
            m = await database_sync_to_async(
                m.prefetch_related)('fields')
            measurement = await database_sync_to_async(
                m.earliest)('date')
        except MeasurementTask.DoesNotExist:
            pass

        if measurement is not None:
            out_serializer = self.out_serializer(measurement)
            await self.send(
                json.dumps(out_serializer.data, ensure_ascii=False))

        self.room_group_name = 'measurement_{}'.format(
            kwargs['s'].contract.contract_id)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def get_measurement(self, content, **kwargs):
        try:
            return MeasurementTask.objects.get(id=content['measurement_id'])
        except MeasurementTask.DoesNotExist:
            return

    async def is_sent(self, content, **kwargs):
        measurement = await self.get_measurement(content, **kwargs)
        if measurement is None:
            await self.send(json.dumps(["Measurement does not exists"]))
            await self.close()
            return

        measurement.is_sent = True
        await database_sync_to_async(measurement.save)()

    async def is_done(self, content, **kwargs):
        measurement = await self.get_measurement(content, **kwargs)
        if measurement is None:
            await self.send(json.dumps(["Measurement does not exists"]))
            await self.close()
            return

        measurement.is_done = True
        await database_sync_to_async(measurement.save)()

    @staticmethod
    def push_value(content, **kwargs):
        aac.add_record(
            kwargs['s'].contract.contract_id,
            content['category_name'],
            content['value'],
        )

    async def receive_json(self, content, **kwargs):
        serializer = self.serializer(data=content)

        if serializer.is_valid():
            try:
                s = await database_sync_to_async(
                    Speaker.objects.select_related('contract').get)(
                    token=serializer.data['token'])
                kwargs['s'] = s
            except Speaker.DoesNotExist:
                await self.send("Invalid token")
                await self.close()
                return

            if serializer.data['request_type'] == 'init':
                return await self.first_init(serializer.data, **kwargs)
            elif serializer.data['request_type'] == 'is_sent':
                return await self.is_sent(serializer.data, **kwargs)
            elif serializer.data['request_type'] == 'is_done':
                return await self.is_done(serializer.data, **kwargs)
            elif serializer.data['request_type'] == 'pushvalue':
                return self.push_value(serializer.data, **kwargs)
            else:
                await self.send(json.dumps(
                    {'request_type': ['Invalid request type']},
                    ensure_ascii=False))
                await self.close()
                return

        await self.send(json.dumps(serializer.errors, ensure_ascii=False))
        await self.close()

    async def receive_measurements(self, event):
        await self.send(json.dumps(event['data'], ensure_ascii=False))


class MedicineNotifyConsumer(AsyncJsonWebsocketConsumer):
    serializer = serializers.IncomingMeasurementNotify
    out_serializer = ma_serializers.MedicineGenericSerializer

    async def connect(self):
        self.room_group_name = None
        self.inited = False
        await self.accept()

    async def disconnect(self, close_code):
        if self.room_group_name is not None:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def first_init(self, content, **kwargs):
        medicine = None
        try:
            m = await database_sync_to_async(
                MedicineTaskGeneric.objects.filter)(
                contract=kwargs['s'].contract, is_sent=False)
            medicine = await database_sync_to_async(
                m.earliest)('date')
        except MedicineTaskGeneric.DoesNotExist:
            pass

        if medicine is not None:
            out_serializer = self.out_serializer(medicine)
            await self.send(
                json.dumps(out_serializer.data, ensure_ascii=False))

        self.room_group_name = 'medicine_{}'.format(
            kwargs['s'].contract.contract_id)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        self.inited = True

    @database_sync_to_async
    def get_medicine(self, content, **kwargs):
        if not (measurement_id := content.get('measurement_id', False)):
            return
        try:
            return MedicineTaskGeneric.objects.get(
                id=measurement_id)
        except MedicineTaskGeneric.DoesNotExist:
            return

    async def is_sent(self, content, **kwargs):
        medicine = await self.get_medicine(content, **kwargs)
        if medicine is None:
            await self.send(json.dumps(["Medicine or specify 'measurement_id'  does not exists"]))
            await self.close()
            return

        medicine.is_sent = True
        await database_sync_to_async(medicine.save)()

    async def is_done(self, content, **kwargs):
        medicine = await self.get_medicine(content, **kwargs)
        if medicine is None:
            await self.send(json.dumps(["Medicine or specify 'measurement_id' does not exists"]))
            await self.close()
            return

        medicine.is_done = True
        await database_sync_to_async(medicine.save)()

    @staticmethod
    def push_value(content, **kwargs):
        aac.add_record(
            kwargs['s'].contract.contract_id,
            'medicine',
            content['value']
        )

    async def receive_json(self, content, **kwargs):
        serializer = self.serializer(data=content)

        if serializer.is_valid():
            try:
                s = await database_sync_to_async(
                    Speaker.objects.select_related('contract').get)(
                    token=serializer.data['token'])
                kwargs['s'] = s
            except Speaker.DoesNotExist:
                await self.send("Invalid token")
                await self.close()
                return

            if serializer.data['request_type'] == 'init':
                return await self.first_init(serializer.data, **kwargs)
            elif self.inited:
                if serializer.data['request_type'] == 'is_sent':
                    return await self.is_sent(serializer.data, **kwargs)
                elif serializer.data['request_type'] == 'is_done':
                    return await self.is_done(serializer.data, **kwargs)
                elif serializer.data['request_type'] == 'pushvalue':
                    return self.push_value(serializer.data, **kwargs)
                else:
                    await self.send(json.dumps(
                        {'request_type': ['Invalid request type']},
                        ensure_ascii=False))
                    await self.close()
                return
            else:
                await self.send(json.dumps(["You must init first"]))
                await self.close()
                return

        await self.send(json.dumps(serializer.errors, ensure_ascii=False))
        await self.close()

    async def receive_medicine(self, event):
        await self.send(json.dumps(event['data'], ensure_ascii=False))
