from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Detector, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)

def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Если пользователь уже авторизован, отправляем его на 'dashboard'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        errors = {}

        # Проверка заполненности полей
        if not username or not email or not password or not password_confirm:
            errors['fields'] = 'Все поля обязательны для заполнения.'

        # Проверка совпадения паролей
        if password != password_confirm:
            errors['password'] = 'Пароли не совпадают.'

        # Проверка уникальности имени пользователя
        if User.objects.filter(username=username).exists():
            errors['username'] = 'Имя пользователя уже занято.'

        # Проверка уникальности email
        if User.objects.filter(email=email).exists():
            errors['email'] = 'Электронная почта уже используется.'

        # Проверка сложности пароля
        try:
            validate_password(password)
        except ValidationError as e:
            errors['password_strength'] = e.messages[0]

        # Если есть ошибки, возвращаем их на страницу
        if errors:
            return render(request, 'register.html', {'errors': errors})

        # Создание пользователя
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Автоматический вход после регистрации
        login(request, user)
        return redirect('dashboard')  # Перенаправление в личный кабинет

    return render(request, 'register.html')

def home(request):
    logger.debug("Домашняя страница загружается")
    return render(request, 'home.html')

@login_required
def dashboard(request):
    user = request.user
    detectors = request.user.owned_detectors.all()
    return render(request, 'dashboard.html', {
        'user': user,
        'detectors': detectors
    })