from django.core.cache import cache
from .models import Product, Category

def get_products_by_category(category_id, limit=None):
    cache_key = f'category_products_{category_id}_{limit or "all"}'
    products = cache.get(cache_key)

    if not products:
        try:
            category = Category.objects.get(id=category_id)
            products = Product.objects.filter(
                category=category,
                is_published=True
            ).select_related('category').only(
                'id', 'name', 'price', 'image', 'category__name'
            )
            if limit:
                products = products[:limit]
            # Сохраняем в кеш (5 минут)
            cache.set(cache_key, list(products), 60 * 5)
        except Category.DoesNotExist:
            products = []
    return products
