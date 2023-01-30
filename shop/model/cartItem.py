from django.db import models;
import uuid

class CartItem(models.Model):
    tag = models.ForeignKey(to="shop.Tag", verbose_name ="商品", null=False, blank=False, on_delete=models.PROTECT, related_name="related_cart_items")
    quantity = models.IntegerField(verbose_name="數量", default=0, null=False, blank=False)
    size = models.ForeignKey(to="shop.Size", verbose_name="尺碼", default=None, null=True, blank=True, on_delete=models.SET_NULL)
    image = models.ForeignKey(to="shop.Image", verbose_name="商品照片", default=None, null=True, blank=True, on_delete=models.DO_NOTHING)
    token = models.UUIDField(default=uuid.uuid4,editable=False, null=False, blank=False)

    def __str__(self):
        return " - ".join([self.related_carts.first().__str__(), self.tag.product.__str__(), str(self.quantity)])

    def createAndSave(tag , size, quantity:int, image):
        if not tag or not quantity > 0:
            return None
        item = CartItem(tag=tag, quantity=quantity, size=size, image=image)
        item.save()
        return item

    def updateQuantityAndSave(self, amount : int):
        self.quantity = amount
        if self.quantity < 0:
            self.quantity = 0
        self.save()

    def getProductBrand(self):
        if self.tag.product:
            return self.tag.product.brand
        return None

    def getProductName(self):
        if self.tag.product:
            return self.tag.product.name
        return None

    def getProductDetailCN(self):
        attributes = []
        if self.tag.color:
            attributes.append(self.tag.color.cn_name)
        if self.size:
            attributes.append(self.size.name)
        if len(attributes) > 0:
            return ' '.join(attributes)
        else:
            return None
        