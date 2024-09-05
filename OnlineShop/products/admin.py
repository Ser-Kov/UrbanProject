from django.contrib import admin
from products.models import ProductCategory, Product, Basket

# Регистрируем модели в админ-панели
admin.site.register(ProductCategory)
# admin.site.register(Product)


# Определяем представление таблицы Product в админ-панели
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    search_fields = ('name',)
    fields = ('name', 'description', ('price', 'quantity'), 'image', 'category')
    list_filter = ('price', 'quantity', 'category')
    ordering = ('name',)


# Используем TabularInline для отображения таблицы в родительской модели (users.admin.UserAdmin)
class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0
