from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import (CategoryProductsView, ContactsView,
                           ProductCreateView, ProductDeleteView,
                           ProductDetailView, ProductListView,
                           ProductUnpublishView, ProductUpdateView)

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path(
        "product_detail/<int:pk>/", ProductDetailView.as_view(), name="product_detail"
    ),
    path("product_create/", ProductCreateView.as_view(), name="product_create"),
    path(
        "product_update/<int:pk>/", ProductUpdateView.as_view(), name="product_update"
    ),
    path(
        "product_delete/<int:pk>/", ProductDeleteView.as_view(), name="product_delete"
    ),
    path(
        "unpublish/<int:pk>/", ProductUnpublishView.as_view(), name="unpublish_product"
    ),
    path(
        "category/<int:pk>/", CategoryProductsView.as_view(), name="category_products"
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
