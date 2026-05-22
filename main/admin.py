from django.contrib import admin

from main.models import ProductCategory, Product, ProductType, ProductType_2
#
#admin.site.register(ProductCategory)
#admin.site.register(Product)
admin.site.register(ProductType)
admin.site.register(ProductType_2)
#
# @admin.register(ProductType_2)
# class PostAdmin(admin.ModelAdmin):
#     list_display = ['name', 'parent_type']
#     ordering = ('parent_type',)
#     search_fields = ['name']
#     list_filter = (
#         'parent_type',)
#     view_on_site = True
#
#
#
@admin.register(ProductCategory)
class PostAdmin(admin.ModelAdmin):
     list_display = ['name', 'description']
     ordering = ('name',)
#     search_fields = ['name']
#     list_filter = (
#         'name',)
#     view_on_site = True
#
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
     list_display = ['name', 'article', 'category', 'price', 'quantity']
#     ordering = ('category',)
     search_fields = ('article', 'name')
#     list_filter = ('quantity')
     list_editable = ('price', 'quantity')
# #




