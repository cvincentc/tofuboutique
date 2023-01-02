from django.shortcuts import render, get_object_or_404, redirect
from shop.models import *

# Create your views here.

def index(request):
    context = {}
    alerts = []
    products = Product.objects.all()
    context['products'] = products
    context['rate'] = 24
    return render(request, 'shop/home/index.html', context)

def products(request):
    context = {}
    alerts = []
    products = Product.objects.all()
    context['products'] = products
    return render(request, 'shop/home/products.html', context)

def brands(request):
    context = {}
    alerts = []
    brands = Brand.objects.filter(selectable=True)
    context['brands'] = brands
    return render(request, 'shop/home/brands.html', context)

def brand(request, slug):
    context = {}
    alerts = []
    parameters = {}
    brand = get_object_or_404(Brand, slug=slug)
    products = Product.objects.filter(brand=brand)
    context['products'] = products
    return render(request, 'shop/home/brand-products.html', context)

def clothes(request):
    return product_by_category(request, 'clothes')

def snacks(request):
    return product_by_category(request, 'snack')

def product_by_category(request, category_str):
    context = {}
    alerts = []
    category = get_object_or_404(Category, name=category_str)
    print(category.related_products.all())
    products = category.related_products.all()
    context['products'] = products
    return render(request, 'shop/home/products.html', context)