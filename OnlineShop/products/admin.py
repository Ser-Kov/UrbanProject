from django.contrib import admin
from products.models import ProductCategory, Product, Basket


admin.site.register(ProductCategory)
# admin.site.register(Product)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    search_fields = ('name',)
    fields = ('name', 'description', ('price', 'quantity'), 'image', 'category')
    list_filter = ('price', 'quantity', 'category')
    ordering = ('name',)


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0
