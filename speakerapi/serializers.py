from rest_framework import serializers

from medsenger_agent.models import Message, Speaker
from speakerapi.models import Firmware


class FirmwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firmware
        fields = '__all__'


class SpeakerSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        request = kwargs.get('context', {}).get('request')

        super().__init__(*args, **kwargs)
        if request:
            if request.META.get('REQUEST_METHOD') != 'POST':
                self.fields['token'] = serializers.CharField(read_only=False)
            if request.META.get('REQUEST_METHOD') == 'GET':
                self.fields['version'] = serializers.CharField(read_only=True)

    code = serializers.CharField(read_only=True)
    token = serializers.CharField(read_only=True)
    # contract = serializers.RelatedField(read_only=True)
    date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Speaker
        exclude = ('contract',)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class CommentSerializer(serializers.Serializer):
    message = serializers.CharField()
    token = serializers.CharField()


class DataSendValuesSerializer(serializers.Serializer):
    category_name = serializers.CharField()
    value = serializers.CharField()


class SendValueSerializer(serializers.Serializer):
    token = serializers.CharField()
    values = serializers.ListField(child=DataSendValuesSerializer())


class CommitMedicineSerializer(serializers.Serializer):
    token = serializers.CharField()
    medicine = serializers.CharField()


class CheckFirmwareSerializer(serializers.Serializer):
    token = serializers.CharField()
    version = serializers.CharField(required=False)


class IncomingMessageNotify(serializers.Serializer):
    token = serializers.CharField()
    notified_message = serializers.BooleanField(required=False)
    message_id = serializers.IntegerField(required=False)
    red_message = serializers.BooleanField(required=False)


class IncomingMeasurementNotify(serializers.Serializer):
    token = serializers.CharField()
    request_type = serializers.CharField()
    measurement_id = serializers.IntegerField(required=False)
    category_name = serializers.CharField(required=False)
    value = serializers.CharField(required=False)


class GetListOfAllCategories(serializers.Serializer):
    token = serializers.CharField()
    names_only = serializers.BooleanField()
