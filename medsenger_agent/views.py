import json
import datetime
import medsenger_api

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render
from django.core import exceptions
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from medsenger_agent import serializers
from medsenger_agent.models import Contract, Speaker, Message
from medsenger_agent import agent_api


APP_KEY = settings.APP_KEY
DOMEN = settings.DOMEN
context = {
    'status': '400', 'reason': 'invalid key'
}
invalid_key_response = HttpResponse(
    json.dumps(context), content_type='application/json')
invalid_key_response.status_code = 400

aac = medsenger_api.AgentApiClient(APP_KEY)


class InitAPIView(CreateAPIView):
    serializer_class = serializers.ContractCreateSerializer

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        return HttpResponse("ok")


class RemoveContractAPIView(GenericAPIView):
    serializer_class = serializers.ContractRemoveSerializer
    queryset = Contract.objects.all()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            try:
                instance = self.get_queryset().get(
                    contract_id=serializer.data['contract_id'])
            except Contract.DoesNotExist:
                raise NotFound(detail="Object not found")
            instance.delete()

            return HttpResponse('ok')


class StatusAPIView(GenericAPIView):
    serializer_class = serializers.StatusSerializer
    queryset = Contract.objects.all()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            data = {
                'is_tracking_data': True,
                'supported_scenarios': [],
                'tracked_contracts': [
                    i.contract_id for i in self.get_queryset()]
            }
            return Response(data)


@require_http_methods(["GET", "POST"])
def settings(request):
    if request.method == "GET":
        if request.GET.get('api_key', '') != APP_KEY:
            return invalid_key_response

        contract_id = request.GET.get('contract_id', '')

    else:
        s_id = request.POST.get('speaker_id', '')
        contract_id = request.POST.get('contract_id', '')

        speaker = Speaker.objects.get(pk=s_id)
        speaker.delete()

    speakers = Speaker.objects.filter(contract=Contract.objects.get(
            contract_id=contract_id))

    return render(request, "settings.html", {
            "contract_id": contract_id,
            "speakers": speakers,
            "api_key": request.GET.get('api_key', ''),
            "len_speakers": len(speakers),
        })


@csrf_exempt
@require_http_methods(["GET", "POST"])
def newdevice(request):
    if request.method == "GET":
        if request.GET.get('api_key', '') != APP_KEY:
            return invalid_key_response

        return render(request, "newdevice.html", {
            "contract_id": request.GET.get('contract_id', ''),
        })

    else:
        code = int(request.POST.get('code', 0))
        contract_id = int(request.POST.get('contract_id', ''))

        try:
            speaker = Speaker.objects.get(code=code)
        except exceptions.ObjectDoesNotExist:
            return render(request, "newdevice.html", {
                "contract_id": contract_id,
                "invalid_code": True,
                "value": code,
            })

        try:
            contract = Contract.objects.get(contract_id=contract_id)
        except exceptions.ObjectDoesNotExist:
            response = HttpResponse(json.dumps({
                'status': 500,
                'reason': 'Contract doesnot exist please reconnect agent',
            }), content_type='application/json')
            response.status_code = 500
            return response

        speaker.contract = contract
        speaker.save()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'auth_%s' % speaker.id,
            {'type': 'receive_authed'}
        )

        return render(request, 'done_add_device.html')


@csrf_exempt
@require_http_methods(["POST"])
def order(request):
    data = json.loads(request.body)
    print(data)

    if data['api_key'] != APP_KEY:
        return invalid_key_response

    try:
        contract = Contract.objects.get(contract_id=data['contract_id'])
    except exceptions.ObjectDoesNotExist:
        response = HttpResponse(json.dumps({
            'status': 400,
            'reason': 'COntract_id does not exist, add agent to this chat'
        }), content_type='application/json')
        response.status_code = 400
        return response

    for measurement in data['params']['measurements']:
        time = None
        if measurement['mode'] == 'daily':
            time = measurement['timetable'][0]['hours']
        elif measurement['mode'] == 'weekly':
            time = measurement['timetable'][0]['days_week']
        else:
            time = measurement['timetable'][0]['days_month']

        for t in time:
            instance = agent_api.get_instance(
                contract,
                measurement['name'],
                measurement['mode'],
                t
            )
            instance = agent_api.check_insatce_task_measurement(
                instance, measurement)
            instance.save()

    return HttpResponse("ok")


class OrderApiView(CreateAPIView):
    serializer_class = serializers.TaskSerializer


class IncomingMessageApiView(APIView):
    serializer_class = serializers.MessageSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                contract = Contract.objects.get(
                    contract_id=serializer.data['contract_id'])
            except exceptions.ObjectDoesNotExist:
                raise ValidationError(detail='Contract does not exist')

            if serializer.data['message']['sender'] == 'patient':
                return HttpResponse("ok")
            date = serializer['message']['date'].value
            message = Message.objects.create(
                contract=contract,
                message_id=serializer.data['message']['id'],
                text=serializer.data['message']['text'],
                date=timezone.localtime(
                    datetime.datetime.strptime(
                        date,
                        "%Y-%m-%d %H:%M:%S").astimezone(timezone.utc)),
            )

            message.save()

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'message_%s' % contract.contract_id,
                {
                    'type': 'receive_message',
                    'message': message.text,
                    'message_id': message.id
                }
            )

            return HttpResponse("ok")
