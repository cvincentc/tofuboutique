from django.shortcuts import render
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
    context['rate'] = 24
    return render(request, 'shop/home/products.html', context)