from django.urls import path
from users.views import login, registration, profile, logout
from products.views import create_order

# Указываем приложение, с которым будут связаны пути.
app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('create_order/', create_order, name='create_order')
]
