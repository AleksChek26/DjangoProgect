from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from catalog.forms import ProductForm
from catalog.models import Product, Category
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .services import get_products_by_category

class CategoryProductsView(ListView):
    model = Product
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'
    paginate_by = 12  # Пагинация: 12 товаров на страницу

    allow_empty = False  # 404, если товаров нет


    def get_queryset(self):
        category_pk = self.kwargs['pk']  # Получаем ID категории из URL
        return get_products_by_category(category_pk, limit=12)  # Фильтруем товары по category_id

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем категорию в контекст
        category_pk = self.kwargs['pk']
        category = get_object_or_404(Category, id=category_pk)
        context['category'] = category
        return context

    # Кеширование всего представления (15 минут)
    @method_decorator(cache_page(60 * 15))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ProductListView(ListView):
    model = Product

@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')
    success_message = "Продукт успешно создан!"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')
    success_message = "Продукт успешно обновлён!"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user:
            return HttpResponseForbidden("У вас нет прав на редактирование этого продукта.")
        return super().dispatch(request, *args, **kwargs)

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        # Модератор или владелец может удалить
        if (request.user.groups.filter(name='Модератор продуктов').exists() or
                obj.owner == request.user):
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("У вас нет прав на удаление.")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Продукт удалён!")
        return super().delete(request, *args, **kwargs)

class ProductUnpublishView(LoginRequiredMixin, DeleteView):  # Используем DeleteView для простоты
    model = Product
    http_method_names = ['post']  # Только POST
    success_url = reverse_lazy('product_list')


    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        # Модератор или владелец может отменить публикацию
        if (request.user.groups.filter(name='Модератор продуктов').exists() or
                obj.owner == request.user):
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("У вас нет прав на отмену публикации.")


    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.is_published = False
        obj.save()
        messages.success(request, "Публикация отменена!")
        return super().delete(request, *args, **kwargs)
