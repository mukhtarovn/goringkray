from django.db import models
from django.urls import reverse


class ProductCategory(models.Model):
    name = models.CharField(verbose_name='имя', max_length=64, unique=True)
    description = models.TextField(verbose_name='описание', blank=True, null=True)
    logo = models.ImageField(verbose_name='логотип', upload_to='products_images', blank=True, null=True, max_length=1000)
    class Meta:
        verbose_name = 'бренд'
        verbose_name_plural = 'бренды'
    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(verbose_name='имя', max_length=64, unique=True)
    description = models.TextField(verbose_name='описание', blank=True, null=True)

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'
    def __str__(self):
        return self.name

class ProductType_2(models.Model):
    name = models.CharField(verbose_name='имя', max_length=64)
    parent_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, null=True, verbose_name='основной тип')
    description = models.TextField(verbose_name='описание', blank=True, null=True)

    class Meta:
        verbose_name = 'Подтип'
        verbose_name_plural = 'подтипы'
    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True)
    article = models.CharField(verbose_name='артикул', max_length= 128, blank=True, null=True)
    name = models.CharField(verbose_name='имя продукта', max_length= 256, null=True)
    series = models.CharField(verbose_name='серия', max_length= 128, blank=True, null=True)
    type = models.ForeignKey(ProductType, on_delete=models.CASCADE, null=True)
    type_2 = models.ForeignKey(ProductType_2, on_delete=models.CASCADE, verbose_name='подтип',blank=True, null=True)
    price = models.PositiveIntegerField(verbose_name='цена', null=True)
    sale_price =models.PositiveIntegerField(verbose_name='цена cо скидкой', null=True, blank=True)
    stock =models.BooleanField(verbose_name='Акция', null=True, blank=True)
    weight = models.CharField(verbose_name='вес', max_length=32, blank=True, null=True)
    short_desc = models.CharField (verbose_name='краткое описание', max_length=200, blank=True)
    igredients = models.CharField(verbose_name='Состав', max_length=2048, blank=True, null=True)
    quantity = models.PositiveIntegerField (verbose_name='количество на складе', default=0)
    image = models.ImageField(verbose_name='фото', upload_to='products_images', blank=True, null=True, max_length=1000)
    image_2 = models.ImageField(verbose_name='фото-2', upload_to='products_images', blank=True, null=True, max_length=1000)
    image_3 = models.ImageField(verbose_name='фото-3', upload_to='products_images', blank=True, null=True, max_length=1000)
    image_4 = models.ImageField(verbose_name='фото-4', upload_to='products_images', blank=True, null=True, max_length=1000)
    image_5 = models.ImageField(verbose_name='фото-5', upload_to='products_images', blank=True, null=True, max_length=200)


    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'

    def get_absolute_url(self):
        return 'https://luchi-sveta.ru/products/product/' +str(self.pk)

    def __str__(self):
        return f'{self.name} ({self.category.name})'
