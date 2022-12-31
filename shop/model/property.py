from django.db import models


class Property(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    value = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return " - ".join(filter(None, (self.name, self.value)))