import medsenger_api

from django.http import HttpResponse
from django.core import exceptions
from django.conf import settings

from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from speakerapi import serializers
from medsenger_agent.models import Speaker, Message


aac = medsenger_api.AgentApiClient(settings.APP_KEY)


class SpeakerInitApiView(APIView):
    def post(self, request, format=None):
        speaker = Speaker.objects.create()
        speaker.save()

        context = {
            'code': speaker.code,
            'token': speaker.token
        }

        return Response(context)


class SpeakerDeleteApiView(APIView):
    def delete(self, request, format=None):
        token = self.request.data.get('token', '')
        try:
            s = Speaker.objects.get(token=token)
        except exceptions.ObjectDoesNotExist:
            raise ValidationError(detail='Invalid Token')
        s.delete()
        return HttpResponse('OK')


"""
class TaskApiView(ListAPIView):
    serializer_class = serializers.TaskSerializer

    def get_queryset(self):
        token = self.request.data.get('token', '')
        try:
            s = Speaker.objects.get(token=token)
            queryset = Task.objects.filter(contract=s.contract)
            return queryset
        except exceptions.ObjectDoesNotExist:
            raise ValidationError(detail='Invalid Token')

    def patch(self, request):
        task_id = self.request.data.get('task_id', '')
        try:
            task = Task.objects.get(pk=int(task_id))
            task.is_done = True
            task.save()
            return HttpResponse("ok")
        except exceptions.ObjectDoesNotExist:
            raise ValidationError(detail='Invalid ID')
"""


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
            return HttpResponse('OK')

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

            return HttpResponse('OK')


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
