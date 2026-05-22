from django.contrib import admin

# Register your models here.
#from django.contrib import admin

#from orderapp.models import Order

#admin.site.register(Order)


from django.contrib import admin
from orderapp.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'status',
        'products_list',
        'created',
        'get_total_quantity',
        'get_total_cost',
    )

    list_filter = (
        'status',
        'created',
    )

    search_fields = (
        'id',
        'user__username',
    )

    inlines = [OrderItemInline]

    def products_list(self, obj):
        return ", ".join(
            [item.product.name for item in obj.orderitem.all()]
        )

    products_list.short_description = 'Товары'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'product',
        'quantity',
        'get_product_cost',
    )
