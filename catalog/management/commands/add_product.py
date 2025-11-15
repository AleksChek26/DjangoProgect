from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Product


class Command(BaseCommand):
    help = "Load test data from fixture"

    def handle(self, *args, **kwargs):
        # Удаляем существующие записи
        Product.objects.all().delete()


class Command(BaseCommand):
    help = "Load test data from fixture"

    def handle(self, *args, **kwargs):
        call_command("loaddata", "product_fixture.json")
        self.stdout.write(self.style.SUCCESS("Successfully loaded data from fixture"))
