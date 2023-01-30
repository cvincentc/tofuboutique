from django.db import models
from ..utils.choice import *
from django.utils.timezone import datetime
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from shop.utils.property import CONVERSION_RATE as conversion_rate
from django.conf import settings
import pytz
import uuid

class Product(models.Model):

    brand = models.ForeignKey(to="shop.Brand", verbose_name = '品牌', null=True, blank=True, on_delete=models.PROTECT, related_name='products_of_brand', default=None)
    retailer = models.ForeignKey(to="shop.Brand", verbose_name = '零售商', null=True, blank=True, on_delete=models.PROTECT, related_name='products_of_retailer', default=None)
    name = models.CharField(verbose_name='商品名字', max_length=100, null=False, blank=False, help_text='*')
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    creation_date = models.DateTimeField(verbose_name = '創建日期', null=True, blank=True, default=datetime.now)
    last_updated = models.DateTimeField(verbose_name = '更新日期', null=True, blank=True, default=datetime.now)
    image_set = models.ManyToManyField(to="shop.Image", verbose_name = '商品照片', related_name='related_products', blank=True)
    category_list = models.ManyToManyField(to="shop.Category", verbose_name = '商品種類', related_name='related_products', blank=True)
    gender = models.CharField(max_length=20, verbose_name = '性別', choices=GenderChoices.choices, default=GenderChoices.UNISEX)
    status = models.CharField(max_length=20, verbose_name = '狀態', choices=ProductStatusChoices.choices, default=ProductStatusChoices.AVAILABLE)
    stock_quantity = models.BigIntegerField(verbose_name = '庫存', default=0)
    
    #prices
    product_price = models.FloatField(verbose_name = '單價',default=0.0, help_text='*')
    retail_price = models.FloatField(verbose_name = '零售價',default=0.0)
    tax_percentage = models.FloatField(verbose_name = '稅率',default=0)
    reference_price = models.FloatField(verbose_name = '平時代購價',default=0.0)
    reference_price_nt = models.FloatField(verbose_name = '平時代購價NT', default=0.0, help_text='*')
    resell_price = models.FloatField(verbose_name = '現代購價', default=0.0)
    resell_price_nt = models.FloatField(verbose_name = '現代購價NT', default=0.0, help_text='*')
    
    customer_viewable = models.BooleanField(verbose_name="客人可見", default=False, null=False, blank=False)

    def __str__(self):
        brand_name = None
        if self.brand:
            brand_name = self.brand.short_name
        return " - ".join(filter(None, [brand_name, self.name, self.status, str(self.stock_quantity)]))

    def update_resell_price(self):
        if self.product_price and self.product_price > 0:
            promotion = self.related_promotions.latest('expire_date')
            if promotion and datetime.now().astimezone(pytz.timezone(settings.TIME_ZONE)) <= promotion.expire_date:
                self.resell_price_nt = promotion.resell_price_nt
                self.resell_price = promotion.resell_price
            else:
                self.resell_price_nt = self.reference_price_nt
                self.reference_price = round(self.reference_price_nt / conversion_rate, 2)
                self.resell_price = self.reference_price
            self.save()
        else:
            raise Exception("Invalid retail price")

@receiver(pre_save, sender=Product)
def product_pre_save(sender, instance : Product, raw, using, **kwargs):
    if not instance.product_price or instance.product_price <= 0 or not instance.resell_price_nt or instance.resell_price_nt <= 0:
        raise Exception("Invalid pricing details")
    else:
        instance.reference_price = round(instance.reference_price_nt / conversion_rate, 2)