from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import RegisterForm, EditAccountForm, PasswordResetForm
from core.utils import generate_hash_key
from courses.models import Enrollment


User = get_user_model()

from  .models import PasswordReset
# Create your views here.
def register(request):
    template_name='register.html'
    
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            form.save()
            return redirect(settings.LOGIN_URL)
        else:
           pass
    else:
        form = RegisterForm()
    
    context={
        'form': form
    }
    return render(request, template_name, context)

@login_required
def dashboard(request):
    template_name='dashboard.html'
    context = {}
    context['form'] = EditAccountForm()
    context['enrollments'] = Enrollment.objects.filter(user=request.user)
    return render(request, template_name, context)

@login_required
def edit_user(request):
    template_name='edituser.html'
    context = {}
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            form = EditAccountForm(instance=request.user)
            context['success'] = True
        else:
            pass   
    else:
        form = EditAccountForm(instance=request.user)
    
    context['form'] = form

    return render(request, template_name, context)


@login_required
def edit_password(request):
    template_name='editpassword.html'
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            context['success'] = True
        else:
            pass   
    else:
        form = PasswordChangeForm(user=request.user)
    
    context['form'] = form

    return render(request, template_name, context)

def password_reset(request):
    template_name="password_reset.html"
    form = PasswordResetForm(request.POST or None)
    context = {}
    if form.is_valid():
        form.save()
        context['success'] = True
    context['form'] = form
    return render(request, template_name, context)

def password_reset_confirm(request, key):
    template_name = 'password_reset_confirm.html'
    context = {}
    reset = get_object_or_404(PasswordReset, key = key)
    form = SetPasswordForm(user = reset.user, data = request.POST or None)
    if form.is_valid():
        form.save()
        context['success'] = True
    context['form'] = form
    return render(request, template_name, context)