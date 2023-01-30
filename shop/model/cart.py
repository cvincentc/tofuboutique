from django.db import models;
from django.utils.timezone import datetime
import uuid

class Cart(models.Model):
    customer = models.ForeignKey(to="shop.Customer", null=True, blank=True, default=None, on_delete=models.CASCADE, related_name='related_carts')
    item_set = models.ManyToManyField(to="shop.CartItem", verbose_name="商品", related_name="related_carts", blank=True)
    last_updated = models.DateTimeField(verbose_name = '更新日期', null=True, blank=True, default=datetime.now)
    checked_out = models.BooleanField(verbose_name="已下單", default=False, null=False, blank=False)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        customer_name = None
        if (self.customer and self.customer.line_display_name):
            customer_name = self.customer.line_display_name
        return " - ".join(filter(None, [customer_name, self.last_updated.strftime('%Y/%m/%d')]))

    def createCartAndSave(customer):
        cart = Cart()
        if customer:
            cart.customer = customer
        cart.save()
        return cart

 
            