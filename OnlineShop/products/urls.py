from django.urls import path
from products.views import products, basket_add, basket_remove, card_product

# Указываем приложение, с которым будут связаны пути.
app_name = 'products'

# Большая часть путей принимают в себя переменные.
urlpatterns = [
    path('', products, name='index'),
    path('page/<int:page_number>', products, name='paginator'), # '/products/page/<int:page_number>'
    path('category/<int:category_id>', products, name='category'), # '/products/category/<int:category_id>'
    path('baskets/add/<int:product_id>', basket_add, name='basket_add'), # '/products/baskets/add/<int:product_id>'
    path('baskets/remove/<int:basket_id>', basket_remove, name='basket_remove'), # '/products/baskets/remove/<int:basket_id>'
    path('card/<int:product_id>', card_product, name='card')
]
