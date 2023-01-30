from django.db import models

class Address(models.Model):
    raw_address = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.raw_address