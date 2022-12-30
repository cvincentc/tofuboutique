from django.db import models
from django.utils.timezone import datetime
from .product import Product

class Promotion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='related_promotions', null=False, blank=False)
    discount_percentage = models.FloatField(default=0)
    additional_discount_percentage = models.FloatField(default=0)
    pre_discount_amount_off = models.FloatField(default=0)
    post_discount_amount_off = models.FloatField(default=0)
    creation_date = models.DateTimeField('creation date', null=True, blank=True, default=datetime.now)
    expire_date = models.DateTimeField(null=True, blank=True, default=datetime.now)

    def __str__(self):
        product_name = None
        if self.product:
            product_name = self.product.name
        return " - ".join(filter(None, (product_name, self.creation_date.strftime('%Y/%m/%d'), self.expire_date.strftime('%Y/%m/%d'))))


