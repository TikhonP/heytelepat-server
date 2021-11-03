from django.contrib.auth import get_user_model
from django.db import models

from medsenger_agent.models import Speaker


class Issue(models.Model):
    description = models.TextField("the issue")
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="the related creator of issue")
    log_file = models.FileField("log for debugging", upload_to='issues/', null=True, blank=True, default=None)
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE, verbose_name="the related speaker")

    date_created = models.DateTimeField("date time created", auto_now_add=True)
    is_closed = models.BooleanField("is issue closed", default=False)

    def __str__(self):
        return self.description
