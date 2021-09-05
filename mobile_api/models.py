from django.db import models

from medsenger_agent.models import Contract


class MedsengerApiToken(models.Model):
    token = models.CharField(max_length=256, unique=True, primary_key=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
