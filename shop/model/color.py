from django.db import models

class Color(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    cn_name = models.CharField(max_length=50, null=False, blank=False, default='unknown')
    def __str__(self):
        return self.name