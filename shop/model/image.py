from django.db import models
from django.utils.timezone import datetime
from .color import Color
from django.db.models.signals import pre_save
from django.dispatch import receiver
from shop.services.wasabi import upload_fileobj
from shop.utils.choice import TokenPrefix
import uuid

class Image(models.Model):
    url = models.CharField(unique=True, max_length=100, default="", blank=True, null=False)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.ImageField(upload_to='images/', null=True, blank=True)
    filename = models.CharField(max_length=50, blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4,editable=False, null=False, blank=False)
    s3_key = models.CharField(max_length=50, editable=False)

    creation_date = models.DateTimeField('creation date', null=True, blank=True, default=datetime.now)

    def __str__(self):
        return " - ".join(filter(None, (self.filename, self.creation_date.strftime('%Y/%m/%d'))))

@receiver(pre_save, sender=Image)
def image_pre_save(sender, instance : Image, raw, using, **kwargs):
    
    if instance.file:
        extension = instance.file.name.split('.')[-1]
        instance.s3_key = str(instance.uuid) + '.' + extension
        instance.url = upload_fileobj(instance.file.file, instance.s3_key)
    instance.file = None