from django.urls import path, include
from django.contrib.auth.views import auth_login
from django.contrib.auth import views as auth_views
from core import views
from accounts import views

app_name='panel'

urlpatterns = [
    path('acessar/',  auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('sair/', auth_views.LogoutView.as_view(next_page='core:home') , name='logout'),
    path('registrar/', views.register, name='register'),
    path('editar/', views.edit_user, name='edituser'),
    path('editar_senha/', views.edit_password, name='editpassword'),
    path('resetar_senha/', views.password_reset, name='passwordreset'),
    path('confirmar_senha/(<str:key>\w+)/', views.password_reset_confirm, name='passwordconfirm'),
    path('dashboard/',  views.dashboard, name='dashboard'),
]