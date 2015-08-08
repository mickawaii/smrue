# -*- encoding:utf-8 -*-

# Usado para encontrar urls
from django.core.urlresolvers import reverse, reverse_lazy

# Usado para verificar permissões
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

# Classes de views
from django.views.generic.base import TemplateView, View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.views.generic.detail import  DetailView
from django.http import HttpResponse, HttpResponseRedirect

from sensor.models import Sensor

class IndexView(ListView):
	template_name = 'sensor/list.html'

	model = Sensor

	context_object_name = 'sensors'

	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)

		context['page_title'] = 'Sensores'

		context['list_title'] = 'Sensores'

		context['create_link'] = reverse_lazy('sensor:create')

		return context

	# @method_decorator(login_required(login_url=reverse_lazy('google_login:login_page')))
	def dispatch(self, *args, **kwargs):
		return super(IndexView, self).dispatch(*args, **kwargs)