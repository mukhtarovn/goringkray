from django.urls import path

import basketapp.views as basketapp

app_name = 'basketapp'

urlpatterns = [
    path('', basketapp.basket, name='basket'),
    path('add/<pk>', basketapp.basket_add, name='add'),
    path('remove/<pk>', basketapp.basket_remove, name='remove'),
    path('edit/<pk>/<quantity>/', basketapp.basket_edit, name='edit'),
    path('update/<int:pk>/', basketapp.update_quantity, name='update'),
]
