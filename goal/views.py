# -*- encoding:utf-8 -*-

# Usado para encontrar urls
from django.core.urlresolvers import reverse, reverse_lazy

# Usado para verificar permissões
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

#Classes de views
from django.views.generic.base import TemplateView, View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.views.generic.detail import  DetailView
from django.http import HttpResponse, HttpResponseRedirect
from goal.forms import GoalForm

#Models
from goal.models import Goal

# Create your views here.
class IndexView(ListView):
	template_name = 'goal/list.html'

	model = Goal

	context_object_name = 'goals'

	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)

		context['page_title'] = 'Listagem de Metas'

		context['list_title'] = 'Listagem de Metas'

		context['create_link'] = reverse_lazy('goal:create')

		return context

	def dispatch(self, *args, **kwargs):
		return super(IndexView, self).dispatch(*args, **kwargs)

class CreateView(CreateView):
	template_name = 'goal/create_form.html'

	model = Goal

	form_class = GoalForm

	success_url = reverse_lazy("goal:list") # Url para redirecionamento

	def get_context_data(self, **kwargs):
		context = super(CreateView, self).get_context_data(**kwargs)

		context['page_title'] = "Nova Meta"

		context['form_title'] = "Nova Meta"
		
		context['editable'] = True

		context['form_button'] = "Salvar"
		context['form_button_class'] = "success"

		context['action_link'] = reverse("goal:create")

		context['back_button'] = "Voltar"

		context['back_link'] = reverse("goal:list")

		return context

	def dispatch(self, *args, **kwargs):
		return super(CreateView, self).dispatch(*args, **kwargs)

class DeleteView(DeleteView):
	model = Goal

	success_url = reverse_lazy("goal:list")

class UpdateView(UpdateView):
	model = Goal
	form_class = GoalForm
	pk_url_kwarg = 'pk'	
	template_name = 'goal/create_form.html'
	success_url = reverse_lazy("goal:list") # Url para redirecionamento

	def get_context_data(self, **kwargs):
		context = super(UpdateView, self).get_context_data(**kwargs)

		context['page_title'] = "Editar Meta"

		context['form_title'] = "Editar Meta"
		
		context['editable'] = True

		context['form_button'] = "Salvar"
		context['form_button_class'] = "success"

		context['back_button'] = "Voltar"

		context['back_link'] = reverse("goal:list")

		return context

	def dispatch(self, *args, **kwargs):
		return super(UpdateView, self).dispatch(*args, **kwargs)