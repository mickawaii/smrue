# -*- encoding:utf-8 -*-

from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import Group, User

class ConfigForm(forms.Form):
	income_type = forms.CharField(label='Tipo de Renda', widget=forms.Select(choices=(('residential','Residencial'),('rural','Rural'),('other_classes','Demais Classes')), attrs={'class': 'form-control'}))
	equipments = forms.CharField(required=False, widget=forms.HiddenInput())
