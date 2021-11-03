from django.contrib import admin

from staff import models


@admin.register(models.Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('description', 'date_created', 'is_closed', 'log_file', 'author')
