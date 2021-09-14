from django.contrib import admin

from speakerapi import models

admin.site.register(models.Firmware)
admin.site.register(models.SpeakerException)