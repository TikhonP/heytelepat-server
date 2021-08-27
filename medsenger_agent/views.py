import json

import medsenger_api
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.core import exceptions
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response

from medsenger_agent import serializers
from medsenger_agent.models import (
    Contract,
    Speaker,
    Message,
    MeasurementTask,
    MeasurementTaskGeneric,
    MedicineTaskGeneric,
)
from speakerapi.serializers import MessageSerializer

APP_KEY = settings.APP_KEY
DOMAIN = settings.DOMAIN
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
            instance = get_object_or_404(
                self.get_queryset(),
                contract_id=serializer.data['contract_id']
            )
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


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def settings(request):
    if request.method == 'GET':
        if request.GET.get('api_key', '') != APP_KEY:
            return invalid_key_response

        contract_id = request.GET.get('contract_id', '')

    else:
        s_id = request.POST.get('speaker_id')
        contract_id = request.POST.get('contract_id')

        speaker = Speaker.objects.get(pk=s_id)
        speaker.delete()

    speakers = Speaker.objects.filter(contract=Contract.objects.get(
        contract_id=contract_id))

    return render(request, 'settings.html', {
        'contract_id': contract_id,
        'speakers': speakers,
        'api_key': request.GET.get('api_key', ''),
        'len_speakers': len(speakers),
        'domain': DOMAIN
    })


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def newdevice(request):
    if request.method == 'GET':
        if request.GET.get('api_key', '') != APP_KEY:
            return invalid_key_response
        return render(request, 'newdevice.html', {
            'contract_id': request.GET.get('contract_id', ''),
            'invalid_code': None,
            'value': None,
        })

    else:
        code = int(request.POST.get('code', 0)) if request.POST.get('code', 0).isdigit() else 0
        contract_id = int(request.POST.get('contract_id', ''))

        try:
            speaker = Speaker.objects.get(code=code)
        except exceptions.ObjectDoesNotExist:
            return render(request, 'newdevice.html', {
                'contract_id': contract_id,
                'invalid_code': True,
                'value': code,
            })

        try:
            contract = Contract.objects.get(contract_id=contract_id)
        except exceptions.ObjectDoesNotExist:
            response = HttpResponse(json.dumps({
                'status': 500,
                'reason': 'Contract does not exist please reconnect agent',
            }), content_type='application/json')
            response.status_code = 500
            return response

        speaker.contract = contract
        speaker.save()

        contract.speaker_active = True
        contract.save()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'auth_%s' % speaker.id,
            {'type': 'receive_authed'}
        )

        return render(request, 'done_add_device.html')


class OrderApiView(GenericAPIView):
    serializer_class = serializers.TaskSerializer

    def post(self, request):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            contract = get_object_or_404(
                Contract,
                contract_id=serializer.data['contract_id']
            )

            if serializer.data['order'] == 'form':
                mt_data = serializer.data['params'].copy()
                mt_data.pop('fields')

                measurement_task = MeasurementTask.objects.create(
                    contract=contract, **mt_data)

                for field in serializer.data['params']['fields']:
                    mtg, create = MeasurementTaskGeneric.objects.get_or_create(
                        value_type=field.pop('type'), **field)
                    measurement_task.fields.add(mtg)

                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'measurement_%s' % contract.contract_id,
                    {
                        'type': 'receive_measurements',
                        'data': serializers.TaskModelSerializer(
                            measurement_task).data
                    }
                )

                return HttpResponse('ok')
            elif serializer.data['order'] == 'medicine':
                m = MedicineTaskGeneric.objects.create(
                    contract=contract,
                    medsenger_id=serializer.data['params'].pop('id'),
                    **serializer.data['params']
                )

                out_serializer = serializers.MedicineGenericSerializer(m)
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'medicine_%s' % contract.contract_id,
                    {
                        'type': 'receive_medicine',
                        'data': out_serializer.data
                    }
                )

                return HttpResponse('ok')
            else:
                raise ValidationError(detail="Invalid order param")


class IncomingMessageApiView(GenericAPIView):
    serializer_class = serializers.MessageSerializer

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data
        )

        if serializer.is_valid(raise_exception=True):
            contract = get_object_or_404(
                Contract,
                contract_id=serializer.data['contract_id']
            )

            if serializer.data['message']['sender'] == 'patient':
                return HttpResponse("ok")

            message = Message.objects.create(
                contract=contract,
                medsenger_id=serializer.data['message'].pop('id'),
                **serializer.data['message']
            )

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'message_%s' % contract.contract_id,
                {
                    'type': 'receive_message',
                    'data': MessageSerializer(message).data
                }
            )

            return HttpResponse("ok")
