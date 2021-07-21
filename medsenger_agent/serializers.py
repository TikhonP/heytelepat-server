import medsenger_api

from django.conf import settings

from rest_framework import serializers

from medsenger_agent.models import (
    MeasurementTask,
    MeasurementTaskGeneric,
    MedicineTaskGeneric,
    Contract,
)


aac = medsenger_api.AgentApiClient(settings.APP_KEY)


class ApiKeyField(serializers.CharField):
    """
    ApiKeyField for api key validation
    """

    def to_internal_value(self, data):
        if isinstance(data, bool) or not isinstance(data, (str, int, float,)):
            self.fail('invalid')
        value = str(data)
        value = value.strip() if self.trim_whitespace else value
        if value != settings.APP_KEY:
            raise serializers.ValidationError('Invalid API key.')
        return value


class TaskGenericSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementTaskGeneric
        fields = '__all__'

    def get_fields(self):
        result = super().get_fields()
        if 'request' in self.context:
            type_ = result.pop('value_type')
            result['type'] = type_
        return result


class MedicineGenericSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        request = kwargs.get('context', {}).get('request')

        super().__init__(*args, **kwargs)
        if request is not None:
            self.fields['id'] = serializers.IntegerField(
                source='medsenger_id', )

    contract = serializers.ReadOnlyField(
        source='contract_id', )

    class Meta:
        model = MedicineTaskGeneric
        exclude = ('date', 'medsenger_id')


class TaskModelSerializer(serializers.ModelSerializer):
    contract = serializers.ReadOnlyField(
        source='contract_id', )
    fields = TaskGenericSerializer(many=True)

    class Meta:
        model = MeasurementTask
        exclude = ('date',)


class TaskSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        request = kwargs.get('context', {}).get('request')
        order = request.data.get('order', '') if request else None

        super().__init__(*args, **kwargs)
        if order == 'form':
            self.fields['params'] = TaskModelSerializer(*args, **kwargs)
        elif order == 'medicine':
            self.fields['params'] = MedicineGenericSerializer(*args, **kwargs)

    api_key = ApiKeyField()
    contract_id = serializers.IntegerField()
    order = serializers.CharField()
    params = TaskModelSerializer()


class MessageDataSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.CharField()
    date = serializers.CharField()
    sender = serializers.CharField()


class MessageSerializer(serializers.Serializer):
    api_key = ApiKeyField()
    contract_id = serializers.IntegerField()
    message = MessageDataSerializer()


class ContractCreateSerializer(serializers.Serializer):
    api_key = ApiKeyField()
    contract_id = serializers.IntegerField()

    def save(self):
        aac.send_message(
            self.validated_data['contract_id'],
            "Зарегистрируйте новое устройство",
            "newdevice", "Добавить", only_patient=True, action_big=True)

        try:
            return Contract.objects.get(
                contract_id=self.validated_data['contract_id'])
        except Contract.DoesNotExist:
            return Contract.objects.create(
                contract_id=self.validated_data['contract_id'])


class ContractRemoveSerializer(serializers.Serializer):
    api_key = ApiKeyField()
    contract_id = serializers.IntegerField()


class StatusSerializer(serializers.Serializer):
    api_key = ApiKeyField()
