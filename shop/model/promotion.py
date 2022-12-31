from django.db import models
from django.utils.timezone import datetime
from .product import Product
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from shop.utils.property import CONVERSION_RATE as conversion_rate
import pytz

class Promotion(models.Model):
    product = models.ForeignKey(Product, verbose_name = '商品', on_delete=models.PROTECT, related_name='related_promotions', null=False, blank=False)
    discount_percentage = models.FloatField(verbose_name = '折扣',default=0)
    additional_discount_percentage = models.FloatField(verbose_name = '折上折',default=0)
    pre_discount_amount_off = models.FloatField(verbose_name = '稅前減價',default=0)
    post_discount_amount_off = models.FloatField(verbose_name = '稅後減價',default=0)
    resell_price = models.FloatField(verbose_name = '售價', default=0, blank=True)
    resell_price_nt = models.FloatField(verbose_name = '售價NT', default=0)
    creation_date = models.DateTimeField(verbose_name = '創建日期', null=True, blank=True, default=datetime.now)
    expire_date = models.DateTimeField(verbose_name = '有效期', null=True, blank=True, default=datetime.now)

    def __str__(self):
        product_name = None
        if self.product:
            product_name = self.product.name
        return " - ".join(filter(None, (product_name, self.creation_date.strftime('%Y/%m/%d'), self.expire_date.strftime('%Y/%m/%d'))))

@receiver(pre_save, sender=Promotion)
def promotion_pre_save(sender, instance : Promotion, raw, using, **kwargs):
    if instance and instance.resell_price_nt and instance.resell_price_nt > 0:
        instance.resell_price = round(instance.resell_price_nt / conversion_rate, 2)

@receiver(post_save, sender=Promotion)
def promotion_post_save(sender, instance : 'Promotion', **kwargs):
    if instance and instance.product and instance.expire_date:
        if datetime.now().astimezone(pytz.timezone(settings.TIME_ZONE)) < instance.expire_date:
            instance.product.update_resell_price()