from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import product_list, contacts, product_detail
from django.conf import settings
from django.conf.urls.static import static


app_name = CatalogConfig.name

urlpatterns = [
    path("", product_list, name="product_list"),
    path("contacts/", contacts, name="contacts"),
    path("product_detail/<int:pk>/", product_detail, name="product_detail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
