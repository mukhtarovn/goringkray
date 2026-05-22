import pandas as pd
from django.core.management.base import BaseCommand
from main.models import Product

class Command(BaseCommand):
    help = "Импорт товаров из Excel"

    def add_arguments(self, parser):
        parser.add_argument("file", type=str, help="Путь к Excel файлу")

    def handle(self, *args, **options):
        file_path = options["file"]
        df = pd.read_excel(file_path)

        for _, row in df.iterrows():
            Product.objects.create(
                name=str(row["name"]).strip(),
                price=row["price"],
                description=str(row.get("description", "")).strip(),
            )

        self.stdout.write(self.style.SUCCESS("Импорт завершён"))