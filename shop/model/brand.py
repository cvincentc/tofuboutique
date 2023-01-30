from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Brand(models.Model):
    name = models.CharField(unique=True, max_length=50, default='Noname', null=False)
    short_name = models.CharField(unique=True, max_length=50, default='N/A', null=False)
    selectable = models.BooleanField(default=False, editable=False)
    logo = models.ForeignKey("shop.Image", null=True, blank=True, on_delete=models.PROTECT, related_name='brand_of_logo', default=None)
    slug = models.SlugField(max_length=100, editable=False, default=None)

    def __str__(self):
        return self.name

@receiver(pre_save, sender=Brand)
def brand_pre_save(sender, instance, raw, using, **kwargs):
    instance.slug = instance.name.replace(' ', '-').lower()