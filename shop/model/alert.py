from django.db import models
from shop.utils.choice import AlertTypeChoices

class Alert(models.Model):
    alert_type = models.CharField(max_length=10, choices=AlertTypeChoices.choices, null=True, blank=True)
    summary = models.CharField(max_length=20, null=True, blank=True)
    detail = models.CharField(max_length=100, null=True, blank=False)

    def __init__(self, alert_type, summary = None, detail = None):
        self.alert_type = alert_type
        self.summary = summary
        self.detail = detail
