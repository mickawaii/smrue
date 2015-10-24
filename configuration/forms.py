# -*- encoding:utf-8 -*-

from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import Group, User
from aes_rate.models import AESRate
from equipment.models import Equipment
from django.db.models import F, Max

from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from smrue.widgets import DatePicker

class ConfigForm(forms.Form):
	income_type_choices = [("", "-----")]+[(val, val) for val in sorted(set(AESRate.objects.annotate(max_valid_date=Max("valid_date")).filter(valid_date=F('max_valid_date')).values_list("name", flat=True)))]
	income_type = forms.CharField(label='Tipo de Renda', widget=forms.Select(choices=income_type_choices, attrs={'class': 'form-control'}))
	equipments = forms.CharField(required=False, widget=forms.HiddenInput())

class UserSetupForm(UserCreationForm):
	username = forms.CharField(required=True, label='Nome de Usuário', widget=forms.TextInput(attrs={'class': 'form-control'}))
	email = forms.EmailField(required=True, label='E-mail', widget=forms.TextInput(attrs={'class': 'form-control'}))
	first_name = forms.CharField(required=False, label='Nome', widget=forms.TextInput(attrs={'class': 'form-control'}))
	last_name = forms.CharField(required=False, label='Sobrenome', widget=forms.TextInput(attrs={'class': 'form-control'}))
	password1 = forms.CharField(required=True, label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	password2 = forms.CharField(required=True, label='Confirme sua Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')        

	def save(self,commit=True):   
		user = super(UserSetupForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']

		if commit:
			user.save()

		return user

class UserEditForm(ModelForm):
	username = forms.CharField(required=True, label='Nome de Usuário', widget=forms.TextInput(attrs={'class': 'form-control'}))
	email = forms.EmailField(required=True, label='E-mail', widget=forms.TextInput(attrs={'class': 'form-control'}))
	first_name = forms.CharField(required=False, label='Nome', widget=forms.TextInput(attrs={'class': 'form-control'}))
	last_name = forms.CharField(required=False, label='Sobrenome', widget=forms.TextInput(attrs={'class': 'form-control'}))

	# extra fields
	income_type = forms.CharField(label='Tipo de Renda', widget=forms.Select(choices=[(val["name"], val["name"]) for val in AESRate.objects.values("name").distinct()], attrs={'class': 'form-control'}))

	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name')    
		exclude = ('password', )    

	def __init__(self, *args, **kwargs):
		super(UserEditForm, self).__init__(*args, **kwargs)

		if Profile.objects.filter(user_id=self.instance.pk).count() == 1:
			self.fields["income_type"].initial = self.instance.profile.income_type

class PasswordEditForm(PasswordChangeForm):
	old_password = forms.CharField(required=True, label='Senha Antiga', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	new_password1 = forms.CharField(required=True, label='Nova Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	new_password2 = forms.CharField(required=True, label='Repita a Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

	class Meta:
		fields = ('old_password', 'new_password1', 'new_password2',)        

class PasswordRecoverForm(PasswordResetForm):
	email = forms.EmailField(required=True, label='E-mail', widget=forms.TextInput(attrs={'class': 'form-control'}))

class PasswordResetForm(SetPasswordForm):
	new_password1 = forms.CharField(label="Nova senha", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	new_password2 = forms.CharField(label="Repita a nova senha", widget=forms.PasswordInput(attrs={'class': 'form-control'}))