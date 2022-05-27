import random
import secrets

from django.contrib.auth import get_user_model
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
    phone = models.CharField(max_length=13, default=None, null=True)

    serial_no = models.CharField(
        "the serial number of speaker",
        max_length=10,
        null=True,
        default=None,
        blank=True,
        unique=True
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True, blank=True,
        default=None, verbose_name="the related user for staff issues",
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.token = secrets.token_urlsafe(16)
            self.code = random.randint(100000, 999999)

        if self.version != 'null' and isinstance(version.parse(str(self.version)), version.LegacyVersion):
            raise ValueError("Version is not valid, got `{}`".format(self.version))

        return super(Speaker, self).save(*args, **kwargs)

    def __str__(self):
        return f"Speaker {self.serial_no} ({self.id})"


class MeasurementTaskGenericRadioVariant(models.Model):
    category = models.CharField(max_length=255)
    category_value = models.TextField()
    custom_params = models.TextField(null=True, blank=True, default=None)
    text = models.TextField()


class MeasurementTaskGeneric(models.Model):
    uid = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    max_value = models.FloatField(null=True)
    min_value = models.FloatField(null=True)
    text = models.CharField(max_length=255)
    value_type = models.CharField(max_length=255)
    prefix = models.CharField(max_length=255, null=True, default=None)
    show_if = models.CharField(max_length=255, null=True, blank=True, default=None)
    variants = models.ManyToManyField(MeasurementTaskGenericRadioVariant)

    def __str__(self):
        return "Category '{}' ({})".format(self.category, self.id)


class MedicineTaskGeneric(models.Model):
    medsenger_id = models.IntegerField()
    title = models.CharField(max_length=255)
    rules = models.TextField("Medicine Task Rules", null=True, blank=True, default=None)
    dose = models.TextField("Medicine dose", null=True, blank=True, default=None)
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
