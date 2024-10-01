import json
from django.shortcuts import render, HttpResponseRedirect
from django.views.decorators.http import require_POST

from products.models import ProductCategory, Product, Basket, Orders
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
@require_POST
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id) # Кнопка "Отправить в корзину" имеет product.id
                                                    # и при нажатии product.id передается в переменную product_id
    baskets = Basket.objects.filter(user=request.user, product=product) # Выберается корзина пользователя с таким продуктом

    count = int(request.POST.get('count', 1))

    if not baskets.exists(): # Если такого товара нет в корзине пользователя, то он создается в кол-ве count
        Basket.objects.create(user=request.user, product=product, quantity=count)
    else: # Если такой товар есть в корзине, то его число увеличивается на count.
        basket = baskets.first()
        basket.quantity += count
        basket.save() # Результат сохраняется

    messages.success(request, 'Товар успешно добавлен в корзину!')

    return HttpResponseRedirect(request.META['HTTP_REFERER'])  # Возвращает пользователя на ту же страницу


# Удаление корзины с продуктами
@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)

    basket.delete()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def create_order(request):
    title = 'Оформление заказа'
    baskets = Basket.objects.filter(user=request.user)

    if request.method == 'POST':
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            index = form.cleaned_data['index']

            for obj in baskets:
                product = Product.objects.get(name=obj.product.name)
                if obj.quantity > product.quantity:
                    messages.error(request, f'Вы не можете заказать {obj.quantity} шт. товара {obj.product.name} '
                                            f'Данного товара на складе: {product.quantity} шт.')
                    return HttpResponseRedirect(request.META['HTTP_REFERER'])

            products_list = []
            for item in baskets:
                products_list.append({
                    'name': item.product.name,
                    'quantity': item.quantity,
                    'price': str(item.product.price),
                })

            # Сериализуем список товаров в JSON
            products_json = json.dumps(products_list, ensure_ascii=False)

            Orders.objects.create(
                user=request.user,
                full_name=full_name,
                email=email,
                address=address,
                city=city,
                index=index,
                products=products_json,
                total_sum=baskets.total_sum())

            # Убираем кол-во продуктов на "складе" равное количеству продуктов в заказе
            for obj in baskets:
                new_quantity = Product.objects.get(name=obj.product.name).quantity - obj.quantity
                Product.objects.filter(name=obj.product.name).update(quantity=new_quantity)

            baskets.delete()

            messages.success(request, 'Заказ оформлен!')
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        form = CreateOrderForm()
    context = {
        'title': title,
        'baskets': baskets,
        'form': form
    }
    return render(request, 'products/create_order.html', context)

def orders_detail(request):
    orders = Orders.objects.filter(user=request.user)

    orders_list = []

    for order in orders:
        products_detail = json.loads(order.products)
        product_list = []

        for dict_ in products_detail:
            product_list.append({
                'product_name': dict_.get("name"),
                'product_price': dict_.get("price"),
                'quantity': dict_.get("quantity"),
            })

        orders_list.append({'id': order.id,
                            'full_name': order.full_name,
                             'email': order.email,
                             'address': order.address,
                             'city': order.city,
                             'index': order.index,
                             'products': product_list,
                            'total_sum': order.total_sum
                            })

    context = {
        'title': 'Заказы',
        'orders': orders_list,
    }

    return render(request, 'users/orders_detail.html', context)

def card_product(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'products/card_product.html', context={'product': product})