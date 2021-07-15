from rest_framework import serializers

from medsenger_agent.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('text', 'id', 'date')


class CommentSerializer(serializers.Serializer):
    message = serializers.CharField()
    token = serializers.CharField()


class DataSendValuesSerializer(serializers.Serializer):
    category_name = serializers.CharField()
    value = serializers.CharField()


class SendValueSerializer(serializers.Serializer):
    token = serializers.CharField()
    values = serializers.ListField(child=DataSendValuesSerializer())


class CheckAuthSerializer(serializers.Serializer):
    token = serializers.CharField()


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
