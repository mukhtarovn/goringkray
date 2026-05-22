from django.conf import settings
from django.db import models

# Create your models here.
from main.models import Product


class Order(models.Model):
    FORMING ='FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDE = 'PRC'
    PAID = 'PD'
    READY = 'RDY'
    DONE = 'DN'
    CANCEL = 'CNC'


    ORDER_STETUSES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'отправлени в обработку'),
        (PROCEEDE, 'обработан'),
        (PAID, 'оплачен'),
        (READY, 'готов к выдаче'),
        (DONE, 'готов'),
        (CANCEL, 'отменен'),

    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updeted = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    status = models.CharField(max_length=3, choices=ORDER_STETUSES, default=FORMING)
    is_active = models.BooleanField(default=True, verbose_name='Активность')

    class META:
        ordering = ('-created')
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'текущий заказ {self.id}'

    def get_total_quantity(self):
        items = self.orderitem.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_product_type_quantity(self):
        items = self.orderitem.select_related()
        return len(items)

    def get_total_cost(self):
        items = self.orderitem.select_related()
        return sum(list(map(lambda x: x.quantity * x.product.price, items)))

    def delete(self):
        for item in self.orderitem.select_related():
            item.product.quantity += item.quantity
            item.product.save()
        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='orderitem', on_delete=models.CASCADE, verbose_name='заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='количество')

    def get_product_cost(self):
        return self.product.price * self.quantity

