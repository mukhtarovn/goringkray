import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taxi.settings')
django.setup()

from main.models import Product

with open('files.txt') as f:
    files = f.read().splitlines()

file_map = {}

for file in files:
    if '.' in file:
        name, ext = file.rsplit('.', 1)
        file_map[name.strip()] = ext

print("Файлов найдено:", len(file_map))

for product in Product.objects.all():
    article = product.article

    if not article:
        continue

    article = article.strip()

    if article in file_map:
        ext = file_map[article]
        product.image = f"products_images/{article}.{ext}"
        product.save()
        print(f"✔ {article} -> {ext}")
