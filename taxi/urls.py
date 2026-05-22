
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from main.views import ProductModelViewSet

import main.views as main

router = DefaultRouter()
router.register('product', ProductModelViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main.main, name='main'),
    path('products/', include('main.urls', namespace='products')),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('basket/', include('basketapp.urls', namespace='basket')),
    path('order/', include('orderapp.urls', namespace='order')),
    path('contacts/', main.contacts, name='contacts'),
    path('price/maytoni/', main.price_maytoni, name='maytoni'),
    path('price/mw/', main.price_mw, name='mw'),
    path('price/lussole/', main.price_lussole, name='lussole'),
    path('price/stluce/', main.price_stluce, name='stluce'),
    path('price/upload/', main.upload, name='upload'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),


    #path('admin/', include('adminapp.urls', namespace='admin'))

]


#if settings.DEBUG:
#    urlpatterns += static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#if settings.DEBUG:

