from django.shortcuts import render
from products.models import ProductCategory, Product


def index(request):
    title = 'Мой онлайн-магазин'
    context = {'title': title}
    return render(request, 'products/index.html', context)


def products(request):
    title = 'My Store - Каталог'
    context = {
        'title': title,
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all()
   }
    return render(request, 'products/products.html', context)

