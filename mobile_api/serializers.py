from rest_framework import serializers

from medsenger_agent.models import Speaker


class CreateSpeakerSerializer(serializers.Serializer):
    api_token = serializers.CharField()
    contract = serializers.IntegerField()


class SpeakerOnlyCodeSerializer(serializers.Serializer):
    class Meta:
        model = Speaker
        fields = ('code',)
