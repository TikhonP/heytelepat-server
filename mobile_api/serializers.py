from rest_framework import serializers


class CreateSpeakerSerializer(serializers.Serializer):
    api_token = serializers.CharField()
    contract = serializers.IntegerField()
