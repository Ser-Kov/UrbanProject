from django.db import models
from django.contrib.auth.models import AbstractUser


# Наследуем модель пользователя от готовой модели AbstractUser, добавляя атрибут для загрузки изображения.
class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
