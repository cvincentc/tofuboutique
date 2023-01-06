from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('brands/', views.brands, name='brands'),
    path('brands/<slug:slug>/', views.brand, name='brand'),
    path('snacks/', views.snacks, name='snacks'),
    path('clothes', views.clothes, name='clothes'),
    path('converter', views.rate_converter, name='converter')
]