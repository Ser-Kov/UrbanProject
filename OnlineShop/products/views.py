import json
from django.shortcuts import render, HttpResponseRedirect
from products.models import ProductCategory, Product, Basket, Orders, BasketSerializer
from products.forms import CreateOrderForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages




# Контроллеры
def index(request):
    title = 'Мой онлайн-магазин'
    context = {'title': title}
    return render(request, 'products/index.html', context)


# Страница каталога с пагинацией и возможностью выбора категории продуктов
def products(request, category_id=None, page_number=1):
    title = 'My Store - Каталог'
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()

    per_page = 3
    paginator = Paginator(products, per_page)
    products_paginator = paginator.page(page_number)

    context = {
        'title': title,
        'products': products_paginator,
        'categories': ProductCategory.objects.all()
   }
    return render(request, 'products/products.html', context)


# Применен декоратор доступа (проверяет request.user на авторизованность).
@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id) # Кнопка "Отправить в корзину" имеет product.id
                                                    # и при нажатии product.id передается в переменную product_id
    baskets = Basket.objects.filter(user=request.user, product=product) # Выберается корзина пользователя с таким продуктом

    if not baskets.exists(): # Если такого товара нет в корзине пользователя, то он создается в кол-ве 1 шт.
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else: # Если такой товар есть в корзине, то его число увеличивается на 1 шт.
        basket = baskets.first()
        basket.quantity += 1
        basket.save() # Результат сохраняется

    return HttpResponseRedirect(request.META['HTTP_REFERER']) # Возвращает пользователя на ту же страницу


# Удаление корзины с продуктами
@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def create_order(request):
    title = 'Оформление заказа'
    if request.method == 'POST':
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            index = form.cleaned_data['index']

            # basket_items = Basket.objects.filter(user=request.user)
            # products_list = []
            # for item in basket_items:
            #     products_list.append(
            #         {'product': item.product.name,
            #          'quantity': item.quantity}
            #     )
            # products_json = json.dumps(products_list, ensure_ascii=False)

            basket_sr = BasketSerializer(Basket.objects.filter(user=request.user), many=True)

            Orders.objects.create(
                user=request.user,
                full_name=full_name,
                email=email,
                address=address,
                city=city,
                index=index,
                products=basket_sr.encode())

            Basket.objects.filter(user=request.user).delete()

            messages.success(request, 'Заказ оформлен!')
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        form = CreateOrderForm()
    context = {
        'title': title,
        'baskets': Basket.objects.filter(user=request.user),
        'form': form
    }
    return render(request, 'products/create_order.html', context)