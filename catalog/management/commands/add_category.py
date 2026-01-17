from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category


class Command(BaseCommand):
    help = "Load test data from fixture"

    def handle(self, *args, **kwargs):
        # Удаляем существующие записи
        Category.objects.all().delete()


class Command(BaseCommand):
    help = "Load test data from fixture"

    def handle(self, *args, **kwargs):
        call_command("loaddata", "category_fixture.json")
        self.stdout.write(self.style.SUCCESS("Successfully loaded data from fixture"))
