from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile


class UserSignUpForm(forms.Form):
    username = forms.CharField(label=False, widget=forms.TextInput(attrs={
        'class':'form-group mb-4 form-control', 'placeholder':'نام کاربری'
    }))
    email = forms.EmailField(label=False, widget=forms.EmailInput(attrs={
        'class':'form-group mb-4 form-control', 'placeholder':'پست الکترونیک'
    }))
    password = forms.CharField(label=False, widget=forms.PasswordInput(attrs={
        'class':'form-group mb-4 form-control ', 'placeholder':'رمز عبور'
    }))
    confirm_password = forms.CharField(label=False, widget=forms.PasswordInput(attrs={
        'class':'form-group mb-4 form-control', 'placeholder':'تکرار رمز عبور'
    }))
    
    def clean_username(self):
        data = self.cleaned_data["username"]
        if User.objects.filter(username=data).exists():
            raise ValidationError('نام کاربری تکراری می باشد')
        return data
    
    def clean_email(self):
        data = self.cleaned_data["email"]
        if User.objects.filter(email=data).exists():
            raise ValidationError('پست الکترونیک تکراری می باشد')
        return data
    
    def clean(self):
        cd = super().clean()
        p = cd.get('password')
        cp = cd.get('confirm_password')
        if p and cp and cp != p:
            raise ValidationError('تکرار رمزعبور مشابه رمزعبور نیست')


class UserSignInForm(forms.Form):
    username = forms.CharField(label=False, widget=forms.TextInput(attrs={
        'class':'form-group mb-4 form-control', 'placeholder':'نام کاربری'
    }))
    password = forms.CharField(label=False, widget=forms.PasswordInput(attrs={
        'class':'form-group mb-4 form-control ', 'placeholder':'رمز عبور'
    }))


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder':'نام کاربری'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'پست الکترونیک'})
        }
        labels = {
            'username': False,
            'email': False
        }
    
    def clean_username(self):
        data = self.cleaned_data["username"]
        if User.objects.filter(username=data).exists():
            raise ValidationError('نام کاربری تکراری می باشد')
        return data
    
    def clean_email(self):
        data = self.cleaned_data["email"]
        if User.objects.filter(email=data).exists():
            raise ValidationError('پست الکترونیک تکراری می باشد')
        return data


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'full_name', 'image', 'address']
        widgets = {
            'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'شماره تماس'}),
            'full_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'نام و نام خانوادگی'}),
            'image': forms.FileInput(attrs={'class':'form-control'}),
            'address': forms.TextInput(attrs={'class':'form-control', 'placeholder':'آدرس'})
        }
        labels = {
            'phone': False,
            'full_name': False,
            'image': False,
            'address': False,
        }
        required = {
            'image': False
        }