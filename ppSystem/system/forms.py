from calendar import c
from re import A
from tkinter import E
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile


class RegisterForm(UserCreationForm):
    # class Meta:
    #     model= User
    #     fields=['username','first_name','last_name','email']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password1"].widget.attrs.update({
            'class': 'register_pw', 'placeholder': 'Enter password'
        })
        self.fields["password2"].widget.attrs.update({
            'class': 'rewrite_pw', 'placeholder': 'Re-enter password'
        })
        self.fields["username"].widget.attrs.update({
            'class': 'register_username', 'placeholder': 'Enter username'
        })

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']
        first_name = forms.CharField()
        last_name = forms.CharField()
        username = forms.CharField()
        email = forms.EmailField()
        password1 = forms.CharField()
        password2 = forms.CharField()


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            'class': 'email', 'placeholder': 'Enter username'
        })
        self.fields["password"].widget.attrs.update({
            'class': 'password', 'placeholder': 'Enter password'
        })

        class Meta:
            model = User
            fields = ['username', 'password']


class ProfileForm(forms.Form):
    candidate_age = forms.IntegerField()
    candidate_phone = forms.IntegerField()
    gender = forms.CharField()
    cv = forms.FileField(allow_empty_file=True)
    oppeness = forms.IntegerField()
    conscientiousness = forms.IntegerField()
    extraversion = forms.IntegerField()
    agreeableness = forms.IntegerField()
    neuroticism = forms.IntegerField()
