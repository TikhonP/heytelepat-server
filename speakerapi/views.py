import medsenger_api
from django.conf import settings
from django.core import exceptions
from django.shortcuts import get_object_or_404
from packaging import version
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from medsenger_agent.models import Speaker, Message, MeasurementTask, MedicineTaskGeneric
from medsenger_agent.serializers import TaskModelSerializer, MedicineGenericSerializer
from speakerapi import serializers
from speakerapi.models import Firmware

aac = medsenger_api.AgentApiClient(settings.APP_KEY)


class InitSpeakerAPIView(GenericAPIView):
    serializer_class = serializers.InitSpeakerSerializer
    queryset = Speaker.objects.all()

    def get(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        speaker = get_object_or_404(self.get_queryset(), code=serializer.data.get('code'))
        contract = speaker.contract
        contract.speaker_active = True
        contract.save()
        return Response({'token': speaker.token})


class SpeakerAPIView(CreateAPIView, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    serializer_class = serializers.SpeakerSerializer
    queryset = Speaker.objects.all()
    token = None

    def get_object(self):
        if self.token is None:
            raise ValidationError(detail='Token required')
        return get_object_or_404(self.get_queryset(), token=self.token)

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.token = serializer.data.get('token')
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.token = serializer.data.get('token')
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.token = serializer.data.get('token')
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.token = serializer.data.get('token')
        return self.destroy(request, *args, **kwargs)


class CheckFirmwareAPIView(GenericAPIView):
    serializer_class = serializers.CheckFirmwareSerializer
    queryset = Firmware.objects.all()

    def get(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not (current_version := serializer.data.get('current_version')):
            raise ValidationError(detail='`Version` required')

        firmware = get_object_or_404(self.get_queryset(), version=current_version)
        out_serializer = serializers.FirmwareSerializer(firmware)
        return Response(out_serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            s = Speaker.objects.get(token=serializer.data['token'])
        except exceptions.ObjectDoesNotExist:
            raise ValidationError(detail='Invalid Token')

        if isinstance((speaker_version := version.parse(s.version)), version.LegacyVersion):
            raise ValidationError(
                detail="Invalid version Speaker `{}`, please update version first.".format(s.version))

        context = {'new_firmware': None}
        firmwares = self.get_queryset().filter(is_active=True)
        for firmware in firmwares:
            firmware_version = version.parse(firmware.version)
            if firmware_version > speaker_version:
                if context.get('new_firmware'):
                    if firmware_version > version.parse(context.get('new_firmware')):
                        context['new_firmware'] = firmware.version
                else:
                    context['new_firmware'] = firmware.version

        return Response(context)


class SendValueAPIView(GenericAPIView):
    serializer_class = serializers.SendValueSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            try:
                s = Speaker.objects.get(
                    token=serializer.data['token'])
            except Speaker.DoesNotExist:
                raise ValidationError(detail='Invalid Token')

            if len(serializer.data['values']) == 1:
                aac.add_record(
                    s.contract.contract_id,
                    serializer.data['values'][0]['category_name'],
                    serializer.data['values'][0]['value'],
                )
            else:
                data = [[i[j] for j in i] for i in serializer.data['values']]
                aac.add_records(
                    s.contract.contract_id,
                    data
                )

            return Response(['ok'])


class SendMessageApiView(APIView):
    serializer_class = serializers.CommentSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.data['message']
        token = serializer.data['token']

        try:
            s = Speaker.objects.get(token=token)
        except exceptions.ObjectDoesNotExist:
            raise ValidationError(detail='Invalid Token')

        message = "Сообщение от пациента: " + message
        aac.send_message(
            s.contract.contract_id, message, need_answer=True, send_from='patient',
        )
        return Response(['ok'])


class CommitMedicineApiView(GenericAPIView):
    serializer_class = serializers.CommitMedicineSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        try:
            s = Speaker.objects.get(
                token=serializer.data['token'])
        except Speaker.DoesNotExist:
            raise ValidationError(detail='Invalid Token')

        aac.add_record(
            s.contract.contract_id,
            'medicine',
            serializer.data['medicine']
        )

        return Response(['ok'])


class IncomingMessageNotifyApiView(GenericAPIView):
    serializer_class = serializers.IncomingMessageNotify

    def get(self, request):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        try:
            s = Speaker.objects.get(token=serializer.data['token'])
        except Speaker.DoesNotExist:
            raise ValidationError(detail='Invalid Token')

        messages = Message.objects.filter(
            contract=s.contract, is_red=False)

        out_serializer = serializers.MessageSerializer(
            messages, many=True)

        for message in messages:
            message.is_red, message.is_notified = True, True
            message.save()

        return Response(out_serializer.data)


class GetListOfAllCategories(APIView):
    serializer_class = serializers.GetListOfAllCategories

    def get(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.data['token']
        names_only = serializer.data['names_only']

        try:
            s = Speaker.objects.get(token=token)
        except exceptions.ObjectDoesNotExist:
            raise ValidationError(detail='Invalid Token')

        data = aac.get_available_categories(s.contract.contract_id)
        if names_only:
            data = [i["name"] for i in data]

        return Response(data)


class MeasurementListAPIView(GenericAPIView):
    queryset = MeasurementTask.objects.all()
    serializer_class = serializers.IncomingMeasurementNotify
    s = None

    def get(self, request):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        try:
            self.s = Speaker.objects.get(token=serializer.data['token'])
        except Speaker.DoesNotExist:
            raise ValidationError(detail='Invalid Token')

        out_serializer = TaskModelSerializer(
            self.get_queryset(), many=True)
        return Response(out_serializer.data)

    # noinspection PyMethodMayBeStatic
    def post(self, request):
        serializer = serializers.SendValueSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        try:
            s = Speaker.objects.get(
                token=serializer.data['token'])
        except Speaker.DoesNotExist:
            raise ValidationError(detail='Invalid Token')

        if len(serializer.data['values']) == 1:
            aac.add_record(
                s.contract.contract_id,
                serializer.data['values'][0]['category_name'],
                serializer.data['values'][0]['value'],
            )
        else:
            data = [[i[j] for j in i] for i in serializer.data['values']]
            aac.add_records(
                s.contract.contract_id,
                data
            )

        return Response(['ok'])

    def patch(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.s = Speaker.objects.get(token=serializer.data['token'])
        except Speaker.DoesNotExist:
            raise ValidationError(detail='Invalid Token')
        if 'measurement_id' not in serializer.data:
            raise ValidationError(detail='Measurement_id missed')

        measurement = get_object_or_404(
            self.get_queryset(),
            id=serializer.data['measurement_id'])
        if serializer.data['request_type'] == 'is_sent':
            measurement.is_sent = True
            measurement.save()
            return Response(TaskModelSerializer(measurement).data)
        elif serializer.data['request_type'] == 'is_done':
            measurement.is_done = True
            measurement.save()
            return Response(TaskModelSerializer(measurement).data)
        else:
            raise ValidationError(detail='Invalid request_type')

    def get_queryset(self):
        return self.queryset.filter(contract=self.s.contract, is_done=False)


class MedicineListAPIView(GenericAPIView):
    queryset = MedicineTaskGeneric.objects.all()
    serializer_class = serializers.IncomingMeasurementNotify
    s = None

    def get(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.s = Speaker.objects.get(token=serializer.data['token'])
        except Speaker.DoesNotExist:
            raise ValidationError(detail='Invalid Token')

        out_serializer = MedicineGenericSerializer(
            self.get_queryset(), many=True)
        return Response(out_serializer.data)

    def patch(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.s = Speaker.objects.get(token=serializer.data['token'])
        except Speaker.DoesNotExist:
            raise ValidationError(detail='Invalid Token')
        if 'measurement_id' not in serializer.data:
            raise ValidationError(detail='Measurement_id missed')

        medicine = get_object_or_404(
            self.get_queryset(),
            id=serializer.data['measurement_id'])

        if serializer.data['request_type'] == 'is_sent':
            medicine.is_sent = True
            medicine.save()
            return Response(MedicineGenericSerializer(medicine).data)
        elif serializer.data['request_type'] == 'is_done':
            medicine.is_done = True
            medicine.save()
            return Response(MedicineGenericSerializer(medicine).data)
        else:
            raise ValidationError(detail='Invalid request_type')

    def get_queryset(self):
        return self.queryset.filter(contract=self.s.contract, is_done=False)
