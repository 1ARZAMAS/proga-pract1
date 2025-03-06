from django.urls import path
from . import views
from .views import logout_view

urlpatterns = [
    path('', views.home, name='home'),  # Домашняя страница
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', logout_view, name='logout'),  # Перенаправление на 'home' после выхода
    path('dashboard/', views.dashboard, name='dashboard'),
]