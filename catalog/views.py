from django.http import HttpResponseForbidden
from django.urls import reverse_lazy

from catalog.forms import ProductForm
from catalog.models import Product
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView


class ProductListView(ListView):
    model = Product

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product

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
