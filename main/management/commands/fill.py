import json
import os
import pandas as pd

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

        types = load_from_json("type")
        ProductType.objects.all().delete()
        for type in types:
            ProductType.objects.create(**type)

        # products = load_from_json("products")
        Product.objects.all().delete()
        # for prod in products:
        #     cat_name = prod["category"]
        #     type_name = prod["type"]
        #     _cat = ProductCategory.objects.get(name=cat_name)
        #
        #     _type = ProductType.objects.get(name=type_name)
        #     prod["category"] = _cat
        #     prod["type"] = _type
        #     Product.objects.create(**prod)



        # products = load_from_json("products_new")
        # for prod in products:
        #     cat_name = prod["category"]
        #     type_name = prod["type"]
        #     _cat = ProductCategory.objects.get (name=cat_name)
        #     _type = ProductType.objects.get (name=type_name)
        #     prod["category"] = _cat
        #     prod["type"] = _type
        #     Product.objects.create (**prod)

        # products = load_from_json("products_stluce")
        # for prod in products:
        #     cat_name = prod["category"]
        #     type_name = prod["type"]
        #     _cat = ProductCategory.objects.get (name=cat_name)
        #     _type = ProductType.objects.get (name=type_name)
        #     prod["category"] = _cat
        #     prod["type"] = _type
        #     Product.objects.create (**prod)

        # products = load_from_json("MV-light")
        # for prod in products:
        #     cat_name = prod["category"]
        #     type_name = prod["type"]
        #     _cat = ProductCategory.objects.get (name=cat_name)
        #     _type = ProductType.objects.get(name=type_name)
        #     prod["category"] = _cat
        #     prod["type"] = _type
        #     Product.objects.create (**prod)



    #ShopUser.objects.all().delete()
    #ShopUser.objects.create_superuser(username='nariman', password='sarvan030511', age=30, first_name='Нариман', )