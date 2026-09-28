from django.conf import settings
from django.db import models

from main.models import Product


class Basket(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )

    session_key = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        db_index=True,
        verbose_name='Сессия'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт'
    )

    quantity = models.PositiveIntegerField(
        verbose_name='Количество',
        default=0
    )

    add_datetime = models.DateTimeField(
        auto_now_add=True
    )

    @staticmethod
    def get_items(user=None, session_key=None):
        if user is not None and user.is_authenticated:
            return Basket.objects.filter(
                user=user
            ).order_by('product__category')

        if session_key:
            return Basket.objects.filter(
                session_key=session_key
            ).order_by('product__category')

        return Basket.objects.none()

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        if self.user and self.user.is_authenticated:
            items = Basket.objects.filter(user=self.user)
        elif self.session_key:
            items = Basket.objects.filter(session_key=self.session_key)
        else:
            items = Basket.objects.none()

        return sum(item.quantity for item in items)

    @property
    def total_cost(self):
        if self.user and self.user.is_authenticated:
            items = Basket.objects.filter(user=self.user)
        elif self.session_key:
            items = Basket.objects.filter(session_key=self.session_key)
        else:
            items = Basket.objects.none()

        return sum(item.product_cost for item in items)

    def __str__(self):
        if self.user:
            owner = str(self.user)
        else:
            owner = f'Гость {self.session_key}'

        return f'{owner} ({self.product} - {self.quantity})'

    @staticmethod
    def get_product(user, product):
        return Basket.objects.filter(
            user=user,
            product=product
        ).first()

    @classmethod
    def get_products_quantity(cls, user):
        basket_items = cls.get_items(user=user)

        basket_item_dic = {
            item.product: item.quantity
            for item in basket_items
        }

        return basket_item_dic