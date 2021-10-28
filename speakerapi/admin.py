from django.contrib import admin

from speakerapi import models


@admin.register(models.Firmware)
class FirmwareAdmin(admin.ModelAdmin):
    list_display = ('version', 'data', 'is_active', 'date')


@admin.register(models.SpeakerException)
class SpeakerExceptionAdmin(admin.ModelAdmin):
    list_display = ('speaker', 'traceback', 'date_created')
