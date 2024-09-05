from django.urls import path
from users.views import login, registration, profile, logout

# Указываем приложение, с которым будут связаны пути.
app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout')
]
