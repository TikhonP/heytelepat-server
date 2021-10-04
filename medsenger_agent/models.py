import random
import secrets

from django.db import models
from packaging import version


class Contract(models.Model):
    contract_id = models.IntegerField(unique=True, primary_key=True)
    speaker_active = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "Contract id - {}".format(self.contract_id)


class Speaker(models.Model):
    code = models.IntegerField(unique=True)
    token = models.CharField(max_length=255, unique=True)
    contract = models.ForeignKey(
        Contract, null=True, default=None, on_delete=models.CASCADE)
    version = models.CharField(default='null', max_length=13)

    def save(self, *args, **kwargs):
        if not self.pk:
            print("Creating new speaker")
            self.token = secrets.token_urlsafe(16)
            self.code = random.randint(100000, 999999)

        if self.version != 'null' and isinstance(version.parse(str(self.version)), version.LegacyVersion):
            raise ValueError("Version is not valid, got `{}`".format(self.version))

        return super(Speaker, self).save(*args, **kwargs)

    def __str__(self):
        return "Speaker `{}` - {}".format(
            self.version, self.id, self.contract)


class MeasurementTaskGeneric(models.Model):
    uid = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    max_value = models.FloatField(null=True)
    min_value = models.FloatField(null=True)
    text = models.CharField(max_length=255)
    value_type = models.CharField(max_length=255)
    prefix = models.CharField(max_length=255, null=True, default=None)

    def __str__(self):
        return "Category '{}' ({})".format(self.category, self.id)


class MedicineTaskGeneric(models.Model):
    medsenger_id = models.IntegerField()
    title = models.CharField(max_length=255)
    rules = models.TextField()
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)

    date = models.DateTimeField(auto_now=True, blank=True)

    is_sent = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return "Medicine ({}) - {}".format(self.id, self.title)


class MeasurementTask(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    doctor_description = models.TextField(null=True, default=None)
    patient_description = models.TextField(null=True, default=None)
    thanks_text = models.TextField(null=True, default=None)
    custom_text = models.TextField(null=True, default=None)
    medsenger_id = models.IntegerField(default=0)
    fields = models.ManyToManyField(MeasurementTaskGeneric)

    is_sent = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)

    date = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return "Measurement ({}) - {}".format(self.id, self.title)


class Message(models.Model):
    contract = models.ForeignKey(
        Contract, on_delete=models.CASCADE, null=True, default=None)

    sender = models.CharField(default='doctor', max_length=255)
    text = models.TextField()
    date = models.DateTimeField()
    medsenger_id = models.IntegerField(default=1)

    is_red = models.BooleanField(default=False)
    is_notified = models.BooleanField(default=False)

    def __str__(self):
        return "Message ({}) - {}".format(self.id, self.text)
