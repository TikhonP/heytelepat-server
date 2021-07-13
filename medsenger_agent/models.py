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


class Task(models.Model):
    contract = models.ForeignKey(
        Contract, on_delete=models.CASCADE, null=True, default=None)

    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255, null=True, default=None)
    unit = models.CharField(max_length=255, null=True, default=None)

    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    MODE_CHOICES = [
        (DAILY, 'DY'),
        (WEEKLY, 'WY'),
        (MONTHLY, 'MY'),
    ]
    mode = models.CharField(max_length=7, choices=MODE_CHOICES)
    last_push = models.DateTimeField(null=True, default=None)
    days_week_day = models.IntegerField(null=True, default=None)
    days_week_hour = models.IntegerField(null=True, default=None)
    hours = models.IntegerField(null=True, default=None)
    days_month_day = models.IntegerField(null=True, default=None)
    days_month_hour = models.IntegerField(null=True, default=None)
    show = models.BooleanField(null=True, default=None)

    max_value = models.FloatField(null=True, default=None)
    min_value = models.FloatField(null=True, default=None)
    # json format {'max_systolic': 160, 'min_systolic': 80,
    # 'max_diastolic': 120, 'min_diastolic': 50, 'max_pulse': 120,
    # 'min_pulse': 40}
    for_pressure_field = models.TextField(null=True, default=None)

    def __str__(self):
        return "{} - {}".format(self.alias, self.contract.contract_id)


class MeasurementTaskGeneric(models.Model):
    uid = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    max_value = models.FloatField(null=True)
    min_value = models.FloatField(null=True)
    text = models.CharField(max_length=255)
    value_type = models.CharField(max_length=255)


class MeasurementTask(models.Model):
    title = models.CharField(max_length=255)
    doctor_description = models.TextField()
    patient_description = models.TextField()
    thanks_text = models.TextField(null=True)
    contract_id = models.ForeignKey(Contract, on_delete=models.CASCADE)
    fields = models.ManyToManyField(MeasurementTaskGeneric)

    is_sent = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)


class Message(models.Model):
    contract = models.ForeignKey(
        Contract, on_delete=models.CASCADE, null=True, default=None)

    message_id = models.IntegerField()
    text = models.TextField()
    date = models.DateTimeField()

    is_red = models.BooleanField(default=False)
    is_notified = models.BooleanField(default=False)
