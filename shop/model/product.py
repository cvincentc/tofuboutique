from django.db import models
from shop.model.brand import Brand
from .image import Image
from .category import Category
from ..utils.choice import *
from django.utils.timezone import datetime
import uuid

class Product(models.Model):

    brand = models.ForeignKey(Brand, null=True, blank=True, on_delete=models.PROTECT, related_name='products_of_brand', default=None)
    retailer = models.ForeignKey(Brand, null=True, blank=True, on_delete=models.PROTECT, related_name='products_of_retailer', default=None)
    name = models.CharField(max_length=100, null=False, blank=False)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    creation_date = models.DateTimeField('creation date', null=True, blank=True, default=datetime.now)
    last_updated = models.DateTimeField('last updated', null=True, blank=True, default=datetime.now)
    image_list = models.ManyToManyField(Image, related_name='related_products', blank=True)
    category_list = models.ManyToManyField(Category, related_name='related_products', blank=True)
    gender = models.CharField(max_length=20, choices=GenderChoices.choices, default=GenderChoices.UNISEX)
    status = models.CharField(max_length=20, choices=ProductStatusChoices.choices, default=ProductStatusChoices.AVAILABLE)
    stock_quantity = models.BigIntegerField(default=0)
    
    #prices
    reference_price = models.FloatField(default=0.0)
    retail_price = models.FloatField(default=0.0)
    resell_price = models.FloatField(default=0.0)
    tax_percentage = models.FloatField(default=0)

    #profit
    promotion_profit_percentage = models.FloatField(default=0.0)
    regular_profit_percentage = models.FloatField(default=0.0)


    def __str__(self):
        brand_name = None
        if self.brand:
            brand_name = self.brand.short_name
        return " - ".join(filter(None, (brand_name, self.name, self.status, self.stock_quantity)))

    def calculate_resell_price(self):
        if self.retail_price and self.retail_price > 0:
            purchase_price = 0
            profit_percentage = 0
            if self.related_promotions:
                promotion = self.related_promotions.latest('expire_date')
                discount_percentage = promotion.discount_percentage | 0
                additional_discount_percentage = promotion.additional_discount_percentage | 0
                pre_discount_amount_off = promotion.pre_discount_amount_off | 0
                post_discount_amount_off = promotion.post_discount_amount_off | 0
                tax_percentage = self.tax_percentage
                purchase_price = \
                    ((self.retail_price - pre_discount_amount_off) \
                    * (100 - discount_percentage) / 100 \
                    * (100 - additional_discount_percentage) / 100
                    - post_discount_amount_off) \
                    * (1 + tax_percentage / 100)
                profit_percentage = self.promotion_profit_percentage
            else:
                purchase_price = self.retail_price * (1 + self.tax_percentage / 100)
                profit_percentage = self.regular_profit_percentage
            self.resell_price = purchase_price * (1 + profit_percentage / 100)
            self.resell_price = round(self.resell_price, 2)
        else:
            raise Exception("Invalid retail price")



