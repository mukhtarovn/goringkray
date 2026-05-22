from django.db import models
from main.models import Product
from taxi import settings


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=0)
    add_datetime = models.DateTimeField(auto_now_add=True, verbose_name='время')

    @staticmethod
    def get_items(user):
        return Basket.objects.filter(user=user).order_by('product__category')

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        _items = Basket.objects.filter(user=self.user)
        _totalquantity = sum(list(map(lambda x: x.quantity, _items)))
        return _totalquantity

    @property
    def total_cost(self):
        _items = Basket.objects.filter(user=self.user)
        _totalcost = sum(list(map(lambda x: x.product_cost, _items)))

        return _totalcost

    def __str__(self):
        return f'{self.user} ({self.product} - {self.quantity})'
    @staticmethod
    def get_product(user, product):
        Basket.objects.filter(user=user, product=product)

    @classmethod
    def get_products_quantity(cls, user):
        basket_items=cls.get_items(user)
        basket_item_dic={}
        [basket_item_dic.update({item.product: item.quantity}) for item in basket_items]
        return basket_items

    def delete(self):
        self.product.quantity += self.quantity
        self.product.save()
