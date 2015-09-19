# -*- encoding:utf-8 -*-

from django.forms import ModelForm
from django import forms
from sensor.models import Sensor
from django.contrib.auth.models import Group, User

class SensorForm(ModelForm):
  name = forms.CharField(required=True, label='Nome', widget=forms.TextInput(attrs={'class': 'form-control'}))

  class Meta:
    model = Sensor
    exclude = ('created_at', 'updated_at', 'code', 'equipment')
