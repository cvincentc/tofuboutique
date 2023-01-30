from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.timezone import datetime

class Customer(models.Model):
    user = models.OneToOneField(User, verbose_name = "用戶", on_delete=models.CASCADE, related_name='related_customer', null=True, blank=True)
    address = models.OneToOneField(to="shop.Address", verbose_name ="地址", on_delete=models.SET_NULL, null=True)
    note = models.CharField(verbose_name ="備註", max_length=500, null=True, blank=True)
    alias = models.CharField(verbose_name ="暱稱", max_length=50, default="", editable=False)
    phone = models.CharField(verbose_name ="電話號碼", max_length=50, null=True, blank=True)
    customer_id = models.CharField(verbose_name ="代號", max_length=50, default="")
    line_user_id = models.CharField(verbose_name="Line Id", max_length=100, editable=False, null=True, blank=True)
    line_display_name = models.CharField(verbose_name="Line用戶名", max_length=50, null=True, blank=True)
    line_profile_pic_url = models.CharField(unique=True, max_length=150, default="", blank=True, null=False)
    token = models.UUIDField(verbose_name ="token", default=uuid.uuid4, editable=False)
    creation_date = models.DateTimeField(verbose_name ="註冊日期", null=True, blank=True, default=datetime.now)
    def __str__(self):
        return " ".join([self.line_display_name, self.customer_id])


    def getMostRecentActiveCart(self):
        return self.related_carts.filter(checked_out=False).first()