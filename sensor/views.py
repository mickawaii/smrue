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
from django.http import HttpResponse, HttpResponseRedirect

from sensor.models import Sensor
from sensor.forms import SensorForm

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

class DeleteView(DeleteView):
	model = Sensor
	success_url = reverse_lazy("sensor:list")

class UpdateView(UpdateView):
	template_name = 'sensor/form.html'

	model = Sensor

	form_class = SensorForm

	success_url = reverse_lazy("sensor:list") # Url para redirecionamento

	def get_context_data(self, **kwargs):
		context = super(UpdateView, self).get_context_data(**kwargs)

		context['page_title'] = "Editar Sensor"

		context['form_title'] = "Editar Sensor"

		context['editable'] = True

		context['form_button'] = "Salvar"
		context['form_button_class'] = "success"

		context['action_link'] = reverse("sensor:edit", kwargs=self.kwargs)

		context['back_button'] = "Voltar"

		context['back_link'] = reverse("sensor:list")

		return context