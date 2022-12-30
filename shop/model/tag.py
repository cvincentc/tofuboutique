from django.db import models
from .product import Product
from .color import Color
from .size import Size
from django.utils.timezone import datetime

class Tag(models.Model):
    product = models.ForeignKey(Product, related_name='related_tags', null=False, blank=False, on_delete=models.PROTECT)
    sku = models.CharField(max_length=50)
    barcode = models.CharField(max_length=50)
    color = models.ForeignKey(Color, related_name='related_tags', on_delete=models.PROTECT)
    size_list = models.ManyToManyField(Size)
    creation_date = models.DateTimeField(null=True, blank=True, default=datetime.now, editable=False)

    def __str__(self):
        product_name = None,
        color = None,
        if self.product:
            product_name = self.product.name
        if self.color:
            color = self.color.name
        return " - ".join(filter(None, (product_name, color, self.sku)))


