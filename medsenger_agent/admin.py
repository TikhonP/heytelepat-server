from django.contrib import admin
from medsenger_agent import models

admin.site.register(models.Contract)
admin.site.register(models.Speaker)
admin.site.register(models.Message)
admin.site.register(models.MeasurementTask)
admin.site.register(models.MeasurementTaskGeneric)
admin.site.register(models.MedicineTaskGeneric)
