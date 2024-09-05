from django.contrib import admin
from django.urls import path, include
from products.views import index
from django.conf.urls.static import static
from django.conf import settings

# Прописываем основные пути и связываем их с путями наших приложений, вынесенных в отдельный файл urls.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('products/', include('products.urls', namespace='products')),
    path('users/', include('users.urls', namespace='users'))
]

# Валидация пути для медиафайлов в режиме локальной разработки (settings.DEBUG = True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)