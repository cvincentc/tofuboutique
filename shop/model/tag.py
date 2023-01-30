from django.db import models
from django.utils.timezone import datetime
import uuid

class Tag(models.Model):
    product = models.ForeignKey(to="shop.Product", related_name='related_tags', null=False, blank=False, on_delete=models.PROTECT)
    sku = models.CharField(max_length=50, blank=True, null=True)
    barcode = models.CharField(max_length=50, blank=True, null=True)
    color = models.ForeignKey(to="shop.Color", related_name='related_tags', on_delete=models.PROTECT, blank=True, null=False)
    size_list = models.ManyToManyField(to="shop.Size", blank=True)
    creation_date = models.DateTimeField(null=True, blank=True, default=datetime.now, editable=False)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        product_name :str = None,
        color :str = '',
        if self.product:
            product_name = self.product.name
        if self.color:
            color = self.color.name
        return " - ".join(filter(None, (product_name, color, self.sku)))


