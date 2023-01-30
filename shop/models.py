from django.db import models
from shop.model.brand import Brand
from shop.model.category import Category
from shop.model.color import Color
from shop.model.image import Image
from shop.model.product import Product
from shop.model.promotion import Promotion
from shop.model.size import Size
from shop.model.tag import Tag
from shop.model.property import Property
from shop.model.address import Address
from shop.model.cart import Cart
from shop.model.cartItem import CartItem
from django.db.models.signals import post_save
from django.dispatch import receiver
from shop.model.cart import Cart
from shop.model.customer import Customer
from shop.model.alert import Alert

@receiver(post_save, sender=Product)
def product_post_save(sender, instance: Product, created, raw, using, **kwargs):
    if created:
        tag = Tag(product = instance, color=Color.objects.get(id=1))
        tag.save()


# Create your models here.
