# -*- encoding:utf-8 -*-

from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import Group, User
from django import forms

class LoginForm(forms.Form):
	username = forms.CharField(max_length=64, label='Usuário', widget=forms.TextInput(attrs={'placeholder': 'Nome do Usuário', 'class': 'form-control'}))
	password = forms.CharField(max_length=64, label='Senha', widget=forms.PasswordInput(attrs={'placeholder': 'Senha', 'class': 'form-control'}))

