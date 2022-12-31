from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products')
]