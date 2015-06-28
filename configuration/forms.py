# -*- encoding:utf-8 -*-

from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import Group, User
from configuration.models import Profile
from equipment.models import Equipment
from django.contrib.auth.forms import UserCreationForm
from smrue.widgets import DatePicker

class ConfigForm(forms.Form):
	income_type = forms.CharField(label='Tipo de Renda', widget=forms.Select(choices=Profile.INCOME_TYPE_CHOICES, attrs={'class': 'form-control'}))
	equipments = forms.CharField(required=False, widget=forms.HiddenInput())

class UserSetupForm(UserCreationForm):
	username = forms.CharField(required=True, label='Nome de Usuário', widget=forms.TextInput(attrs={'class': 'form-control'}))
	email = forms.EmailField(required=True, label='E-mail', widget=forms.TextInput(attrs={'class': 'form-control'}))
	first_name = forms.CharField(required=False, label='Nome', widget=forms.TextInput(attrs={'class': 'form-control'}))
	last_name = forms.CharField(required=False, label='Sobrenome', widget=forms.TextInput(attrs={'class': 'form-control'}))
	birthday = forms.DateField(required=False, label='Data de Nascimento', widget=DatePicker(format='%d/%m/%Y', attrs={'placeholder': 'dd/mm/yyyy', 'class': 'form-control'}))
	password1 = forms.CharField(required=True, label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	password2 = forms.CharField(required=True, label='Confirme sua Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

	income_type = forms.CharField(label='Tipo de Renda', widget=forms.Select(choices=Profile.INCOME_TYPE_CHOICES, attrs={'class': 'form-control'}))

	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')        

	def save(self,commit=True):   
		user = super(UserSetupForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.birthday = self.cleaned_data['birthday']

		if commit:
			user.save()

		return user