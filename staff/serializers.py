from rest_framework import serializers


class InitSpeakerSerializer(serializers.Serializer):
    token = serializers.CharField()
