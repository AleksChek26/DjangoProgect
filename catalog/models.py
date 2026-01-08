from django.db import models
from django.db.models import SET_NULL
from django.conf import settings


def get_default_owner():
    from django.contrib.auth import get_user_model
    User = get_user_model()
    return User.objects.get_or_create(email='system_owner')[0].id

class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to="images", blank=True, null=True, verbose_name="Изображение")
    category = models.ForeignKey(
        "Category",
        on_delete=SET_NULL,
        verbose_name="Категория",
        null=True,
        blank=True,
        related_name="products",
    )
    price = models.PositiveIntegerField(verbose_name="Цена продукта")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего изменения"
    )
    is_published = models.BooleanField(default=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products',
        default=get_default_owner
    )

    def __str__(self):
        return f"{self.name} {self.category}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name"]
        permissions = [
            ("can_unpublish_product", "Может отменять публикацию продукта"),
        ]


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return f"{self.name} {self.description}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]
