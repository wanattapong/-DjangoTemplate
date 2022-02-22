from ast import Try
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm, ChangeForm
from django.urls import resolve
import os

# Create your views here.


def is_admin(user):
    if user.groups.all()[0].name == 'Admin':
        return True
    else:
        return False

def login_view(request):
    if request.method == 'POST':
        valuenext= request.POST.get('next', '')
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if valuenext:
                return redirect(resolve(valuenext).url_name)
            else:
                if is_admin(user):
                    return redirect('home-admin')
                else:
                    return redirect('profile')
    else:
        form = LoginForm()
    return render(request, 'singin.html', dict(form = form))

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user_obj = form.save()
        user_obj.groups.add(Group.objects.get(name='User'))
        return redirect('singin')
    return render(request, "register.html", dict(form = form))

def logout_view(request):
    logout(request)
    return redirect('singin')

@login_required()
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('change_password')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', dict(form = form))

@login_required()
def profile_view(request):
    if request.method == "POST" and request.is_ajax() and not request.FILES:
        form = ChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.update()
            return JsonResponse({'status':'true'}, status=201)
        else:
            return JsonResponse({'status':'false', 'error': form.errors}, status=500)
    elif request.method == "POST" and request.is_ajax() and request.FILES:
        image = request.FILES.get('avatar')
        try:
            os.remove(request.user.avatar.path)
        except:
            pass
        request.user.avatar = image
        request.user.save(update_fields=['avatar'])
        return JsonResponse({'status':'true'}, status=201)
    else:
        form = ChangeForm(user=request.user)
        return render(request, 'profile.html', dict(form = form))