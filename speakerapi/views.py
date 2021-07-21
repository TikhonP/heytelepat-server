import medsenger_api

from django.core import exceptions
from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from speakerapi import serializers
from medsenger_agent.models import Speaker, Message, MeasurementTask, MedicineTaskGeneric
from medsenger_agent.serializers import TaskModelSerializer, MedicineGenericSerializer


aac = medsenger_api.AgentApiClient(settings.APP_KEY)


class SpeakerInitApiView(APIView):
    def post(self, request):
        speaker = Speaker.objects.create()
        speaker.save()

        context = {
            'code': speaker.code,
            'token': speaker.token
        }

        return Response(context)


class SpeakerDeleteApiView(APIView):
    def delete(self, request):
        token = self.request.data.get('token', '')
        try:
            s = Speaker.objects.get(token=token)
        except exceptions.ObjectDoesNotExist:
            raise ValidationError(detail='Invalid Token')
        s.delete()
        return Response(['ok'])


class SendMessageApiView(APIView):
    serializer_class = serializers.CommentSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            message = serializer.data['message']
            token = serializer.data['token']

            try:
                s = Speaker.objects.get(token=token)
            except exceptions.ObjectDoesNotExist:
                raise ValidationError(detail='Invalid Token')

            message = "Сообщение от пациента: " + message
            aac.send_message(
                s.contract.contract_id, message, need_answer=True)
            return Response(['ok'])

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendValueApiView(GenericAPIView):
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


class CommitMedicineApiView(GenericAPIView):
    serializer_class = serializers.CommitMedicineSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
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

        if serializer.is_valid(raise_exception=True):
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
        if serializer.is_valid(raise_exception=True):
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

    def get(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            try:
                self.s = Speaker.objects.get(token=serializer.data['token'])
            except Speaker.DoesNotExist:
                raise ValidationError(detail='Invalid Token')

            out_serializer = TaskModelSerializer(
                self.get_queryset(), many=True)
            return Response(out_serializer.data)

    def patch(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
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

    def get(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            try:
                self.s = Speaker.objects.get(token=serializer.data['token'])
            except Speaker.DoesNotExist:
                raise ValidationError(detail='Invalid Token')

            out_serializer = MedicineGenericSerializer(
                self.get_queryset(), many=True)
            return Response(out_serializer.data)

    def patch(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            try:
                self.s = Speaker.objects.get(token=serializer.data['token'])
            except Speaker.DoesNotExist:
                raise ValidationError(detail='Invalid Token')
            if 'measurement_id' not in serializer.data:
                raise ValidationError(detail='Measurement_id missed')

            medicine = get_object_or_404(
                self.get_queryset(),
                medsenger_id=serializer.data['measurement_id'])

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