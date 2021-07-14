from django.db import models
import secrets
import random


class Contract(models.Model):
    contract_id = models.IntegerField(unique=True, primary_key=True)
    speaker_active = models.BooleanField(default=False)

    def __str__(self):
        return "Contract id - {}".format(self.contract_id)


class Speaker(models.Model):
    code = models.IntegerField(unique=True)
    token = models.CharField(max_length=255, unique=True)
    contract = models.ForeignKey(
        Contract, null=True, default=None, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.pk:
            print("Creating new speaker")
            self.token = secrets.token_urlsafe(16)
            self.code = random.randint(100000, 999999)

        return super(Speaker, self).save(*args, **kwargs)


class MeasurementTaskGeneric(models.Model):
    uid = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    max_value = models.FloatField(null=True)
    min_value = models.FloatField(null=True)
    text = models.CharField(max_length=255)
    value_type = models.CharField(max_length=255)


class MedicineTaskGeneric(models.Model):
    medsenger_id = models.IntegerField()
    title = models.CharField(max_length=255)
    rules = models.TextField()
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)

    date = models.DateTimeField(auto_now_add=True, blank=True)

    is_sent = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)


class MeasurementTask(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    doctor_description = models.TextField(null=True, default=None)
    patient_description = models.TextField(null=True, default=None)
    thanks_text = models.TextField(null=True, default=None)
    fields = models.ManyToManyField(MeasurementTaskGeneric)

    is_sent = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)

    date = models.DateTimeField(auto_now_add=True, blank=True)


class Message(models.Model):
    contract = models.ForeignKey(
        Contract, on_delete=models.CASCADE, null=True, default=None)

    message_id = models.IntegerField()
    text = models.TextField()
    date = models.DateTimeField()

    is_red = models.BooleanField(default=False)
    is_notified = models.BooleanField(default=False)
