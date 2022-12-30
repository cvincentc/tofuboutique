from django.db import models

class Brand(models.Model):
    name = models.CharField(unique=True, max_length=50, default='Noname', null=False)
    short_name = models.CharField(unique=True, max_length=50, default='N/A', null=False)

    def __str__(self):
        return self.name