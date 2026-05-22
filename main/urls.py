
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

import main.views as main

app_name = 'main'

urlpatterns = [
    path('', main.products, name='index'),
    path('category/<int:pk>/', main.products, name='category'),
    path('type/<int:pk>/', main.types, name='type'),
    path('type/<int:pk>/<int:page>/', main.types, name='type_page'),
    path('category/<int:pk>/<int:page>/', main.products, name='page'),
    path('product/<int:pk>/', main.product, name='product'),
    path('search/', main.search_result, name='search'),
    path('info/', main.info, name='info'),
    path('sales/', main.sales, name='sales'),
    path('sales/<int:page>/', main.sales, name='sales_page'),
]
