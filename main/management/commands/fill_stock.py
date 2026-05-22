import json
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import BaseCommand

from authapp.models import ShopUser
from main.models import ProductCategory, Product, ProductType

FILE_PATH = os.path.join(settings.BASE_DIR, 'main/json')

def load_from_json(file_name):
    with open(os.path.join(FILE_PATH, file_name + '.json')) as json_file:
        return json.load(json_file)

class Command(BaseCommand):

    def handle(self, *args, **options):
        # categories = load_from_json("categories")
        # ProductCategory.objects.all().delete()
        # for cat in categories:
        #     ProductCategory.objects.create(**cat)
        #
        # types = load_from_json("type")
        # ProductType.objects.all().delete()
        # for type in types:
        #     ProductType.objects.create(**type)

        products = load_from_json("products")
        for prod in products:
            try:
                _article = prod['article']
                _price = prod['price']
                _quantity = prod['quantity']
            except KeyError:
                _quantity = 0
            Product.objects.filter(article=_article).update(price=_price, quantity=_quantity)

        products = load_from_json("products_new")
        for prod in products:
            try:
                _sale_price = None
                _article = prod['article']
                _price = prod['price']
                _quantity = prod['quantity']
                if prod['sale_price']:
                    _sale_price=prod['sale_price']

            except KeyError:
                _quantity = 0
            Product.objects.filter(article=_article).update (price=_price, quantity=_quantity, sale_price=_sale_price)

        products = load_from_json("products_stluce")
        for prod in products:
            try:
                _sale_price = None
                _article = prod['article']
                _price = prod['price']
                _quantity = prod['quantity']
                if prod['sale_price']:
                    _sale_price = prod['sale_price']
                Product.objects.filter (article=_article).update (price=_price, quantity=_quantity,
                                                                  sale_price=_sale_price)

            except:
                pass

            # Product.objects.filter (article=_article).update (price=_price, quantity=_quantity, sale_price=_sale_price)

        products = load_from_json("MV-light")
        for prod in products:
            try:
                _sale_price = None
                _article = prod['article']
                _price = prod['price']
                _quantity = prod['quantity']
                if prod['sale_price']:
                    _sale_price = prod['sale_price']
            except:
                pass
            Product.objects.filter (article=_article).update (price=_price, quantity=_quantity, sale_price=_sale_price)

        products = load_from_json ("VeleLuce")
        for prod in products:
            try:
                _sale_price = None
                _article = prod['article']
                _price = prod['price']
                _quantity = prod['quantity']
                if prod['sale_price']:
                    _sale_price = prod['sale_price']
            except:
                pass

            Product.objects.filter (article=_article).update (price=_price, quantity=_quantity, sale_price=_sale_price)

    # products = load_from_json ("electrostandard")
        # for prod in products:
        #     _article = prod['article']
        #     _price = prod['price']
        #     _quantity = prod['quantity']
        # Product.objects.filter (article=_article).update (price=_price, quantity=_quantity)

        # products = load_from_json ("eurosvet")
        # for prod in products:
        #     _article = prod['article']
        #     _price = prod['price']
        #     _quantity = prod['quantity']
        # Product.objects.filter (article=_article).update (price=_price, quantity=_quantity)
        products = load_from_json ("Lussole")
        for prod in products:
            try:
                _sale_price = None
                _article = prod['article']
                _price = prod['price']
                _quantity = prod['quantity']
                if prod['sale_price']:
                    _sale_price = prod['sale_price']
            except:
                pass

            Product.objects.filter (article=_article).update (price=_price, quantity=_quantity, sale_price=_sale_price)

    #ShopUser.objects.all().delete()
    #ShopUser.objects.create_superuser(username='nariman', password='sarvan030511', age=30, first_name='Нариман', )