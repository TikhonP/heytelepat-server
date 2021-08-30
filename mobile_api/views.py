import requests
from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from medsenger_agent.models import Speaker, Contract
from mobile_api import serializers
from django.conf import settings


class CreateNewSpeakerAPIView(GenericAPIView):
    serializer_class = serializers.CreateSpeakerSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.data.get('api_token') != settings.APP_KEY:
            url = settings.MAIN_HOST + '/api/client/doctors'
            answer = requests.get(url, params={'api_token': serializer.data.get('api_token')})
            if not answer.ok or answer.json()['state'] != 'success':
                raise ValidationError("Error with checking api_token: {}".format(answer.json()['error']))

            contracts = [i['contract'] for i in answer.json()['data']]

            if serializer.data['contract'] not in contracts:
                raise ValidationError("Invalid api_token for given contract")

        contract, _ = Contract.objects.get_or_create(contract_id=serializer.data['contract'])
        speaker = Speaker.objects.create(contract=contract)

        return Response({'code': speaker.code})
