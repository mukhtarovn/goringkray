from django.contrib import admin

from authapp.models import ShopUser

#admin.site.register(ShopUser)

@admin.register(ShopUser)
class PostAdmin(admin.ModelAdmin):
    list_display = ['username', 'last_name', 'first_name', 'phone', 'email']
    ordering = ('last_name',)
    search_fields = ['last_name', 'first_name']
    list_filter = (
        ('phone', admin.EmptyFieldListFilter),
        ('email', admin.EmptyFieldListFilter),)