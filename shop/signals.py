from models import *
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import boto3

@receiver(pre_save, sender=Image)
def image_pre_save(sender, instance : Image, raw, using, **kwargs):
    print('hello')
    if instance.file:
        extension = instance.file.name.split('.')[-1]
    s3 = boto3.resource('s3')
    for bucket in s3.buckets.all():
        print(bucket.name)
        print(extension)
        instance.file = None

@receiver(post_save, sender=Promotion)
def promotion_post_save(sender, instance : 'Product', created, raw, using, **kwargs):
    if created:
        instance.calculate_resell_price()