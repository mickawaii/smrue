# -*- encoding:utf-8 -*-

from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse, reverse_lazy
from django.http.response import HttpResponse
from forms import LoginForm

from django.contrib import messages
import json
from collections import OrderedDict

class HomeView(TemplateView):
	template_name = 'home.html'

	def get_context_data(self, **kwargs):
		context = super(HomeView, self).get_context_data(**kwargs)

		context['page_title'] = 'SMRUE'

		context['current_user'] = self.request.user

		return context

class LoginView(FormView):
	template_name = 'login.html' # Nome do template a ser usado

	form_class = LoginForm

	sucess_url = reverse_lazy('home')

	# Se usuário já loggado, redirecionar para home
	def get(self, *args, **kwargs):
		user = self.request.user

		if user.is_authenticated():
			return HttpResponseRedirect(reverse('home'))
		else:
			return super(LoginView, self).get(*args, **kwargs)

	# Contexto do template a ser usado
	def get_context_data(self, **kwargs):
		context = super(LoginView, self).get_context_data(**kwargs)

		context['page_title'] = 'Fazer Login'

		context['form_title'] = 'Login'

		context['form_button'] = 'Fazer Login'
		
		context['editable'] = True

		context['action_link'] = reverse("login")

		context['back_link'] = reverse("home")

		context['back_button'] = "Voltar a página principal"
		
		return context

	def form_valid(self, form):
		username = form['username'].value()
		password = form['password'].value()

		user = authenticate(username=username, password=password)
		if user is not None:
			login(self.request, user)
			return HttpResponseRedirect(self.sucess_url)
		else:
			pass
			messages.error(self.request, 'Usuário ou senha incorretos.')
			return HttpResponseRedirect(reverse('login'))

class LogoutView(View):
	def get(self, request):
		user = self.request.user

		if user.is_authenticated():
			logout(request)
			return HttpResponseRedirect(reverse('home'))
		else:
			return HttpResponseRedirect(reverse('login'))