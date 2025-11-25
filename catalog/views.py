from lib2to3.fixes.fix_input import context

from django.shortcuts import render, get_object_or_404

from catalog.models import Product


def product_list(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "product_list.html", context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product}
    return render(request, "product_detail.html", context)


def contacts(request):
    return render(request, "contacts.html")
