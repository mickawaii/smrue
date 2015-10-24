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
from equipment.models import Equipment
from consumption.models import Consumption
from equipment.forms import EquipmentForm

class IndexView(ListView):
	template_name = 'equipment/list.html'

	model = Equipment

	context_object_name = 'equipments'

	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)

		context['page_title'] = 'Equipamentos'

		context['list_title'] = 'Equipamentos'

		context['create_link'] = reverse_lazy('equipment:create')

		return context

	# @method_decorator(login_required(login_url=reverse_lazy('google_login:login_page')))
	def dispatch(self, *args, **kwargs):
		return super(IndexView, self).dispatch(*args, **kwargs)

class CreateView(CreateView):
	template_name = 'equipment/form.html'

	model = Equipment

	form_class = EquipmentForm

	success_url = reverse_lazy("equipment:list") # Url para redirecionamento

	def get_context_data(self, **kwargs):
		context = super(CreateView, self).get_context_data(**kwargs)

		context['page_title'] = "Novo Equipamento"

		context['form_title'] = "Novo Equipamento"

		context['editable'] = True

		context['form_button'] = "Salvar"
		context['form_button_class'] = "success"

		context['action_link'] = reverse("equipment:create")

		context['back_button'] = "Voltar"

		context['back_link'] = reverse("equipment:list")

		return context

	def dispatch(self, *args, **kwargs):
		return super(CreateView, self).dispatch(*args, **kwargs)

class UpdateView(UpdateView):
	template_name = 'equipment/form.html'

	model = Equipment

	form_class = EquipmentForm

	success_url = reverse_lazy("equipment:list") # Url para redirecionamento

	def get_context_data(self, **kwargs):
		context = super(UpdateView, self).get_context_data(**kwargs)

		context['page_title'] = "Editar Equipamento"

		context['form_title'] = "Editar Equipamento"

		context['editable'] = True

		context['form_button'] = "Salvar"
		context['form_button_class'] = "success"

		context['action_link'] = reverse("equipment:edit", kwargs=self.kwargs)

		context['back_button'] = "Voltar"

		context['back_link'] = reverse("equipment:list")

		return context

	def dispatch(self, *args, **kwargs):
		return super(UpdateView, self).dispatch(*args, **kwargs)

class DeleteView(DeleteView):
	model = Equipment
	success_url = reverse_lazy("equipment:list")
