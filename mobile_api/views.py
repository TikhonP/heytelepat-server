import requests
from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from medsenger_agent.models import Speaker, Contract
from mobile_api import serializers
from mobile_api.models import MedsengerApiToken
from speakerapi.serializers import SpeakerSerializer


def validate_api_key(api_token: str, contract: int) -> Contract:
    """Validate medsenger api_key with medsenger request."""

    try:
        return MedsengerApiToken.objects.get(token=api_token).contract
    except MedsengerApiToken.DoesNotExist:
        url = settings.MAIN_HOST + '/api/client/doctors'
        answer = requests.get(url, params={'api_token': api_token})
        if not answer.ok or answer.json()['state'] != 'success':
            raise ValidationError("Error with checking api_token: {}".format(answer.json()['error']))

        contracts = [i['contract'] for i in answer.json()['data']]

        if contract not in contracts:
            raise ValidationError("Invalid api_token for given contract")

        contract_obj, _ = Contract.objects.get_or_create(contract_id=contract)
        MedsengerApiToken.objects.create(
            token=api_token, contract=contract_obj
        )
        return contract_obj


class CreateNewSpeakerAPIView(GenericAPIView):
    serializer_class = serializers.CreateSpeakerSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.data.get('api_token') == settings.APP_KEY:
            contract, _ = Contract.objects.get_or_create(contract_id=serializer.data['contract'])
        else:
            contract = validate_api_key(**serializer.data)

        speaker = Speaker.objects.create(contract=contract)
        return Response({'code': speaker.code})

    def put(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contract = validate_api_key(**serializer.data)

        speakers = Speaker.objects.filter(contract=contract)
        out_serializer = SpeakerSerializer(speakers, many=True)
        return Response(out_serializer.data)
