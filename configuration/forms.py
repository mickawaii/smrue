# -*- encoding:utf-8 -*-

from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import Group, User
from configuration.models import Profile
from equipment.models import Equipment

class ConfigForm(forms.Form):
	income_type = forms.CharField(label='Tipo de Renda', widget=forms.Select(choices=Profile.INCOME_TYPE_CHOICES, attrs={'class': 'form-control'}))
	equipments = forms.CharField(required=False, widget=forms.HiddenInput())

class UserForm(ModelForm):
	income_type = forms.CharField(label='Tipo de Renda', widget=forms.Select(choices=Profile.INCOME_TYPE_CHOICES, attrs={'class': 'form-control'}))
	name = forms.CharField(required=True, label='Nome', widget=forms.TextInput(attrs={'class': 'form-control'}))
	nominal_power = forms.DecimalField(required=True, label='Valor Nominal', widget=forms.TextInput(attrs={'class': 'form-control js-money'}))
	measurement_unit = forms.CharField(max_length=5, label='Unidade de Medida', widget=forms.Select(choices=Equipment.MEASUREMENT_UNITS, attrs={'class': 'form-control'}))
	approximated_consumption = forms.DecimalField(required=True, label='Consumo Aproximado', widget=forms.TextInput(attrs={'class': 'form-control'}))
	description = forms.CharField(required=False, label='Descrição', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))

	class Meta:
		model = User
		exclude = ('user',)
