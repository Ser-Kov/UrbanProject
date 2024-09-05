from django.contrib import admin
from users.models import User
from products.admin import BasketAdmin

# admin.site.register(User)


# Включаем в UserAdmin дочернюю модель BasketAdmin,
# ранее определив ее с помощью класса TabularInline (products.admin.BasketAdmin)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    inlines = (BasketAdmin,)