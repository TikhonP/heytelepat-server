from django.db import models
from packaging import version


class Firmware(models.Model):
    version = models.CharField(max_length=13, unique=True)
    data = models.FileField(upload_to='firmwares/')
    is_active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if isinstance(version.parse(self.version), version.LegacyVersion):
            raise ValidationError("Version is not valid, got `{}`".format(self.version))

        return super().save(*args, **kwargs)

    def __str__(self):
        return str("Active " if self.is_active else "Disabled ") + str(self.version)
