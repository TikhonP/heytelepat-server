from django.contrib import admin

from medsenger_agent import models


@admin.register(models.Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('contract_id', 'speaker_active', 'is_active')


@admin.register(models.Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('serial_no', 'contract', 'version', 'user')


admin.site.register(models.Message)
admin.site.register(models.MeasurementTask)
admin.site.register(models.MeasurementTaskGeneric)
admin.site.register(models.MedicineTaskGeneric)
