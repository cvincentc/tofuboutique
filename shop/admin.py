from django.contrib import admin
from shop.models import *

Models = (Brand, Category, Color, Image, Product, Promotion, Size, Tag, Property, Cart, CartItem)

# Register your models here.
admin.site.register(Models)