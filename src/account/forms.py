from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import User
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

    # class Meta:
    #     model = User
    #     fields = ['username', 'password']

    def clean(self):
        # cleaned_data = super().clean()
        username_ = self.cleaned_data['username']
        password_ = self.cleaned_data['password']
        user = authenticate(username=username_, password=password_)
        if user:
            if not user.is_active:
                raise ValidationError("The account not is disabled.")
        else:
            raise ValidationError("Invalid username or password.")
        return self.cleaned_data

    def get_user(self):
        # cleaned_data = super().clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        return user

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2','email']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("ชื่อผู้ใช้นี้ได้รับการลงทะเบียนแล้ว")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("อีเมลนี้ได้รับการลงทะเบียนแล้ว.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("รหัสผ่านไม่ตรงกัน.")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = True
        # is_superuser = True
        user.save()
        # save user profile
        # Profiles.objects.create(user=user)
        return user

class ChangeForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangeForm, self).__init__(*args, **kwargs)

    # class Meta:
    #     model = User
    #     fields = ['username', 'first_name', 'last_name', 'email']

    username = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    avatar = forms.ImageField(required=False)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exclude(pk=self.user.id).exists():
            raise ValidationError("ชื่อผู้ใช้นี้ได้รับการลงทะเบียนแล้ว")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(pk=self.user.id).exists():
            raise ValidationError("อีเมลนี้ได้รับการลงทะเบียนแล้ว.")
        return email

    def update(self):
        self.user.username = self.cleaned_data.get('username')
        self.user.first_name = self.cleaned_data.get('first_name')
        self.user.last_name = self.cleaned_data.get('last_name')
        self.user.email = self.cleaned_data.get('email')
        self.user.save(update_fields=['username', 'first_name', 'last_name', 'email'])
        return self.user

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField()
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            return email
        else:
            raise ValidationError("ไม่พบอีเมลนี้ในระบบ.")
    
class SetPasswordForm(SetPasswordForm):

    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("รหัสผ่านไม่ตรงกัน.")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['new_password1'])
        if commit:
            user.save()
        return user