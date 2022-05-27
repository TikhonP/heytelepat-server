import medsenger_api
from django.conf import settings
from rest_framework import serializers

from medsenger_agent.models import (
    MeasurementTask,
    MeasurementTaskGeneric,
    MedicineTaskGeneric,
    Contract,
    Message,
    MeasurementTaskGenericRadioVariant
)

aac = medsenger_api.AgentApiClient(settings.APP_KEY)


class ApiKeyField(serializers.CharField):
    """ApiKeyField for api key validation"""

    def to_internal_value(self, data):
        if isinstance(data, bool) or not isinstance(data, (str, int, float,)):
            self.fail('invalid')
        value = str(data)
        value = value.strip() if self.trim_whitespace else value
        if value != settings.APP_KEY:
            raise serializers.ValidationError('Invalid API key.')
        return value


class MeasurementTaskGenericRadioVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementTaskGenericRadioVariant
        fields = '__all__'


class TaskGenericParamsSerializer(serializers.Serializer):
    variants = MeasurementTaskGenericRadioVariantSerializer(many=True, required=False, read_only=True)

class TaskGenericSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        # request = kwargs.get('context', {}).get('request')

        super().__init__(*args, **kwargs)
        # print(self.context)
        # if request:
        #     print("hh:", request.data.get('fields'))
        # else:
        #     print("request.data.get('fields')")
        #     print(kwargs, kwargs.get('context'))
        #     print(self.fields)
        # if request and request.META.get('REQUEST_METHOD') == 'POST':
        #     self.fields['params'] = serializers.IntegerField(source='medsenger_id')

    params = TaskGenericParamsSerializer()

    class Meta:
        model = MeasurementTaskGeneric
        fields = '__all__'

    def get_fields(self):
        result = super().get_fields()
        if 'request' in self.context:
            type_ = result.pop('value_type')
            result['type'] = type_
        result.pop('variants')
        return result


class MedicineGenericSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        request = kwargs.get('context', {}).get('request')

        super().__init__(*args, **kwargs)

        if request is not None:
            self.fields['id'] = serializers.IntegerField(source='medsenger_id')

    contract = serializers.ReadOnlyField(
        source='contract_id', )

    class Meta:
        model = MedicineTaskGeneric
        exclude = ('date', 'medsenger_id')


class TaskModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        request = kwargs.get('context', {}).get('request')

        super().__init__(*args, **kwargs)

        # print(self.context)
        if request and request.META.get('REQUEST_METHOD') == 'POST':
            self.fields['id'] = serializers.IntegerField(source='medsenger_id')
        # self.fields['fields'] = TaskGenericSerializer(many=True)

    contract = serializers.ReadOnlyField(source='contract_id')
    fields = TaskGenericSerializer(many=True, )

    class Meta:
        model = MeasurementTask
        exclude = ('date',)


# noinspection PyAbstractClass
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


class MessageDataSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        request = kwargs.get('context', {}).get('request')

        super().__init__(*args, **kwargs)
        if request is not None:
            self.fields['id'] = serializers.IntegerField(source='medsenger_id')

    date = serializers.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'])

    class Meta:
        model = Message
        fields = ('sender', 'text', 'date')


class MessageSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'] = MessageDataSerializer(*args, **kwargs)

    api_key = ApiKeyField()
    contract_id = serializers.IntegerField()
    message = MessageDataSerializer()


class ContractCreateSerializer(serializers.Serializer):
    api_key = ApiKeyField()
    contract_id = serializers.IntegerField()

    def save(self):
        instance, created = Contract.objects.get_or_create(contract_id=self.validated_data.get('contract_id'))
        if not created:
            instance.is_active = True
            instance.save()

        return instance


class ContractRemoveSerializer(serializers.Serializer):
    api_key = ApiKeyField()
    contract_id = serializers.IntegerField()


class StatusSerializer(serializers.Serializer):
    api_key = ApiKeyField()
