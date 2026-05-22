from django.urls import re_path

import orderapp.views as orderapp

app_name = 'orderapp'

urlpatterns = [
   re_path(r'^$', orderapp.OrderList.as_view(), name='order_list'),
   re_path(r'^forming/complete/(?P<pk>\d+)/$', orderapp.order_forming_complete, name='order_forming_complete'),
   re_path(r'^create/$', orderapp.OrderItemsCreate.as_view(), name='order_create'),
   re_path(r'^read/(?P<pk>\d+)/$', orderapp.OrderRead.as_view(), name='order_read'),
   re_path(r'^update/(?P<pk>\d+)/$', orderapp.OrderItemsUpdate.as_view(), name='order_update'),
   re_path(r'^delete/(?P<pk>\d+)/$', orderapp.OrderDelete.as_view(), name='order_delete'),
]