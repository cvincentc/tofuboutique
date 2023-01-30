from typing import Set
from shop.models import *

def getProductImageSetInColorSet(product: Product, color_set: Set[Color]):
    image_set = []
    if product.image_set:
        for image in product.image_set.all():
            if image.color in color_set:
                image_set.append(image)
    return image_set

def getProductImageSetInColorStrSet(product: Product, color_set_str: Set[str]):
    color_set = Color.objects.filter(name__in=color_set_str)
    return getProductImageSetInColorSet(product, color_set)

def addItemAndSave(cart, tag, size, quantity, image):
    if not tag:
        return False
    item: CartItem = cart.item_set and cart.item_set.filter(tag=tag, size=size).first()
    if item:
        item.updateQuantityAndSave(item.quantity + quantity)
    else:
        item = CartItem.createAndSave(tag, size, quantity, image)
        if not item:
            return False
        cart.item_set.add(item)
    if item.quantity <= 0:
        cart.item_set.remove(item)
    cart.save()
    return True