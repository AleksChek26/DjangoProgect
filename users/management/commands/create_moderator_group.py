from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создаёт группу "Модератор продуктов" и назначает права'

    def handle(self, *args, **kwargs):
        content_type = ContentType.objects.get_for_model(Product)
        unpublish_perm = Permission.objects.get(
            codename="can_unpublish_product",
            content_type=content_type,
        )
        delete_perm = Permission.objects.get(
            codename="delete_product",
            content_type=content_type,
        )

        group, created = Group.objects.get_or_create(name="Модератор продуктов")
        if created:
            self.stdout.write(self.style.SUCCESS("Группа создана"))
        else:
            self.stdout.write("Группа уже существует")

        group.permissions.add(unpublish_perm, delete_perm)
        self.stdout.write(self.style.SUCCESS("Права назначены"))
