from turtle import pen
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm, ChangeForm, PasswordResetRequestForm, SetPasswordForm
from django.urls import resolve
from django.core.files.storage import default_storage
from .models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.exceptions import ValidationError
# Email
from django.core import mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string

# Create your views here.

def is_admin(user):
    if user.groups.all()[0].name == 'Admin':
        return True
    else:
        return False

@login_required()
def profile_view(request):
    if request.method == "POST" and request.is_ajax() and not request.FILES:
        form = ChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.update()
            return JsonResponse({'status':'true'}, status=200)
        else:
            return JsonResponse({'status':'false', 'error': form.errors}, status=500)
    elif request.method == "POST" and request.is_ajax() and request.FILES:
        image = request.FILES.get('avatar')
        if default_storage.exists(request.user.avatar.path) == True and request.user.avatar != "":
            default_storage.delete(request.user.avatar.path)
        request.user.avatar = image
        request.user.save(update_fields=['avatar'])
        return JsonResponse({'status':'true'}, status=200)
    else:
        form = ChangeForm(user=request.user)
        return render(request, 'profile.html', dict(form = form))

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

def password_reset_request(request):
    if request.method == 'POST' and request.is_ajax():
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email=form.cleaned_data['email'])
            context = {
                'name' : user.get_full_name,
                'protocol': 'http',
                'domain': request.get_host(),
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': PasswordResetTokenGenerator().make_token(user),
                }
            subject = "อีเมลล์ตอบรับคำร้องเปลี่ยนรหัสผ่าน"
            html_message = render_to_string('email/email_request_reset_password.html', context)
            plain_message = strip_tags(html_message)
            to = user.email
            mail.send_mail(subject, plain_message, None, [to], html_message=html_message)

            return JsonResponse({'status':'true'}, status=200)
        else:
            return JsonResponse({'status':'false', 'error': form.errors}, status=500)
    else:
        form = PasswordResetRequestForm()
        return render(request, 'password_reset_request.html', dict(form = form))

def password_reset(request, uidb64, token):
    uid = urlsafe_base64_decode(uidb64).decode()
    user = get_object_or_404(User, pk=uid)

    if PasswordResetTokenGenerator().check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user=user, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('singin')
        else:
            form = SetPasswordForm(user=user)
        return render(request, 'password_reset.html', dict(form = form, uidb64 = uidb64, token = token))
    else:
        return HttpResponse("Invalid token")