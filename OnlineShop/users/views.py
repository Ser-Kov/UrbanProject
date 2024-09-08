from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from products.models import Basket
from django.contrib.auth.decorators import login_required


# Контроллер авторизации с использованием формы users.forms.UserLoginForm
def login(request):
    title = 'Авторизация'
    if request.method == 'POST': # Если происходит отправка данных
        form = UserLoginForm(data=request.POST) # Вставляем данные в форму из request.POST
        if form.is_valid(): # Проверка валидации данных формы
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password) # user=bool (аутентификация)
            if user: # Если пользователь существует
                auth.login(request, user) # Вход
                return HttpResponseRedirect(reverse('index')) # Возврат на главную страницу
    else:
        form = UserLoginForm() # Изначально GET-запрос, получает форму.

    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'users/login.html', context)


# Контроллер регистрации с использованием формы users.forms.UserRegistrationForm
def registration(request):
    title = 'Регистрация'
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрированы!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {
        'title': title,
        'form': form
    }
    return render(request, 'users/registration.html', context)


# Контроллер профиля с использованием формы users.forms.UserProfileForm
@login_required
def profile(request):
    title = 'Профиль'
    if request.method == 'POST':
        # В форму вставляем изначальные данные пользователя (instance=request.user)
        # Для загрузки файлов передаем параметр files=request.FILES
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
            # return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)
    context = {'title': title,
               'form': form}
    # В baskets (шаблон: 'products/baskets.html') передаем корзину текущего пользователя
    # во избежание представления корзин других пользователей
    return render(request, 'users/profile.html', context)


# Выход из системы
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))

def baskets(request):
    title = 'Корзина'
    context = {'title': title,
               'baskets': Basket.objects.filter(user=request.user)}
    return render(request, 'products/baskets.html', context)
