from django.db import models
from users.models import User
from rest_framework import serializers


# Модель с категориями (class Meta нужен для корректного отображения названия модели в админ-панели)
class ProductCategory(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


# Модель продуктов. Связываем с категориями (ForeignKey) - каждый продукт будет иметь одну из категорий.
# Продуктов много - категория одна.
class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return f'Продукт: {self.name} | Цена: {self.price} | Категория: {self.category.name}'


# Создаем класс, определяя в нем новые методы QuerySet для менеджера Basket.objects
class BasketQuerySet(models.QuerySet):
    def total_sum(self): # Возвращает итоговую сумму цен всех продуктов в корзине
        return sum(basket.sum() for basket in self)

    def total_quantity(self): # Возвращает итоговое количество продуктов в корзине
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager() # Добавляем в objects созданный класс-менеджер с новыми методами

    def __str__(self):
        return f'Корзина пользователя {self.user.username} | Продукт: {self.product.name}| Количество: {self.quantity}'

    def sum(self): # Возвращает итоговую сумму конкретного продукта в корзине
        return self.product.price * self.quantity


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = ('product.name', 'product.price', 'quantity')

    def encode(self):
        from rest_framework.renderers import JSONRenderer
        json = JSONRenderer().render(self.data)
        return json


class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=128)
    city = models.CharField(max_length=30)
    index = models.CharField(max_length=6)
    products = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def __str__(self):
        return f'Заказ от {self.user.username}. Город: {self.city}'

