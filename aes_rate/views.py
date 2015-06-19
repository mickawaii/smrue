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

class IndexView(ListView):
	# template_name = 'equipment/list.html'

	# model = Equipment

	# context_object_name = 'equipments'

	# def get_context_data(self, **kwargs):
	# 	context = super(IndexView, self).get_context_data(**kwargs)

	# 	context['page_title'] = 'Listagem de Equipamentos'

	# 	context['list_title'] = 'Listagem de Equipamentos'

	# 	context['create_link'] = reverse_lazy('equipment:create')


	# 	return context

	# def get_queryset(self):
	# 	queryset = Equipment.objects.all()

	# 	return queryset

	# # @method_decorator(login_required(login_url=reverse_lazy('google_login:login_page')))
	# def dispatch(self, *args, **kwargs):
	# 	return super(IndexView, self).dispatch(*args, **kwargs)
