from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ContactsView, ProductDetailView
from django.conf import settings
from django.conf.urls.static import static


app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("product_detail/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
