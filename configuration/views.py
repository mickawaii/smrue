# -*- encoding:utf-8 -*-

# Usado para encontrar urls
from django.core.urlresolvers import reverse, reverse_lazy

# Usado para verificar permissões
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

# Classes de views
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import RedirectView

from sensor.models import Sensor
from equipment.models import Equipment
from configuration.models import Profile
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from configuration.forms import ConfigForm, UserSetupForm, UserEditForm, PasswordEditForm, PasswordRecoverForm, PasswordResetForm
import json
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db import transaction
from smrue.helpers import send_email
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class ConfigView(TemplateView):
	template_name = 'configuration/config.html'

	def get_context_data(self, **kwargs):
		context = super(ConfigView, self).get_context_data(**kwargs)

		context['page_title'] = 'Minhas configurações'

		context['action_link'] = reverse_lazy("configuration:config")

		income_type = None
		if hasattr(self.request.user, 'profile'):
			income_type = self.request.user.profile.income_type

		context['form'] = ConfigForm(initial={'income_type': income_type})

		context['equipments'] = Equipment.objects.all()

		context['has_sensors'] = Sensor.objects.count() > 0

		context['free_sensors'] = Sensor.objects.filter(equipment_id__isnull=True)

		return context

	def post(self, request):
		equipments = json.loads(request.POST.get("equipments"))
		income_type = request.POST.get("income_type", None)

		if income_type:
			Profile.objects.update_or_create(user=request.user,defaults={"income_type":income_type})

		with transaction.atomic():
			for obj in equipments:
				equipment = get_object_or_404(Equipment, pk=obj["equipment"])
				old_sensor = Sensor.objects.filter(equipment_id=obj["equipment"])
				new_sensor = obj["sensor"]

				if old_sensor.count() > 0:
					old_sensor = old_sensor.first()

					if not new_sensor:
						old_sensor.equipment = None
						old_sensor.save()
					elif new_sensor:
						new_sensor = Sensor.objects.filter(pk=obj["sensor"]).first()

						if new_sensor.id != old_sensor.id:
							old_sensor.equipment_id = None
							old_sensor.save()
							new_sensor.equipment = equipment
							new_sensor.save()
							
				elif new_sensor:
					new_sensor = Sensor.objects.filter(pk=obj["sensor"]).first()
					new_sensor.equipment = equipment
					new_sensor.save()

		return HttpResponseRedirect(reverse_lazy("configuration:config"))

	# @method_decorator(login_required(login_url=reverse_lazy('google_login:login_page')))
	def dispatch(self, *args, **kwargs):
		return super(ConfigView, self).dispatch(*args, **kwargs)

class UserCreateView(CreateView):
	template_name = 'configuration/user.html'

	model = User

	form_class = UserSetupForm

	success_url = reverse_lazy("home") # Url para redirecionamento

	def get_context_data(self, **kwargs):
		context = super(UserCreateView, self).get_context_data(**kwargs)

		context['page_title'] = 'Registro de Usuário'

		context['form_title'] = 'Registro de Usuário'

		context['action_link'] = reverse_lazy("configuration:create_user")

		context['form_button'] = "Salvar"
		context['form_button_class'] = "success"

		context['editable'] = True

		return context

	def form_valid(self, form):
		user = form.save()
		username = form['username'].value()
		password = form['password1'].value()

		user = authenticate(username=username, password=password)
		login(self.request, user)

		return HttpResponseRedirect(reverse("home"))

	def dispatch(self, *args, **kwargs):
		return super(UserCreateView, self).dispatch(*args, **kwargs)

class UserUpdateView(FormView):
	template_name = 'configuration/user.html'

	model = User

	form_class = UserEditForm

	success_url = reverse_lazy("home") # Url para redirecionamento

	def get_form(self):
		if self.request.POST:
			form = self.form_class(self.request.POST, instance=self.request.user)
		else:
			form = self.form_class(instance=self.request.user)

		return form

	def get_context_data(self, **kwargs):
		context = super(UserUpdateView, self).get_context_data(**kwargs)

		context['page_title'] = 'Minha conta'

		context['form_title'] = 'Minha conta'

		context['action_link'] = reverse_lazy("configuration:edit_user")

		context['form'] = self.get_form()

		context['form_button'] = "Salvar"
		context['form_button_class'] = "success"

		context['change_password_button'] = True
		context['editable'] = True

		return context

	def form_valid(self, form):
		user = form.save()
		income_type = form.cleaned_data["income_type"]

		if income_type:
			Profile.objects.update_or_create(user=user,defaults={"income_type":income_type})

		messages.success(self.request, 'Dados alterados com sucesso.')

		return HttpResponseRedirect(reverse_lazy("configuration:edit_user"))

	def dispatch(self, *args, **kwargs):
		return super(UserUpdateView, self).dispatch(*args, **kwargs)

class PasswordUpdateView(FormView):
	template_name = 'configuration/user.html'

	model = User

	form_class = PasswordEditForm

	success_url = reverse_lazy("home") # Url para redirecionamento

	def get_form(self):
		if self.request.POST:
			form = self.form_class(data=self.request.POST, user=self.request.user)
		else:
			form = self.form_class(user=self.request.user)

		return form

	def get_context_data(self, **kwargs):
		context = super(PasswordUpdateView, self).get_context_data(**kwargs)

		context['page_title'] = 'Alterar senha'

		context['form_title'] = 'Alterar senha'

		context['form'] = self.get_form()

		context['action_link'] = reverse_lazy("configuration:edit_password")

		context['back_button'] = "Voltar"

		context['back_link'] = reverse_lazy("configuration:edit_user")

		context['form_button'] = "Salvar"
		context['form_button_class'] = "success"

		context['form_button1'] = "Alterar Senha"

		context['editable'] = True

		return context

	def form_valid(self, form):
		form.save()
		messages.success(self.request, 'Senha alterada com sucesso.')

		return HttpResponseRedirect(reverse_lazy("configuration:edit_user"))

	def dispatch(self, *args, **kwargs):
		return super(PasswordUpdateView, self).dispatch(*args, **kwargs)

class PasswordRecoverView(FormView):
	def recover_password(self, request):
		context = super(PasswordRecoverView, self).get_context_data()
		context['page_title'] = 'Reconfigurar a senha'
		context['form_title'] = 'Reconfigurar a senha'
		context['action_link'] = reverse_lazy("configuration:recover_password")
		context['back_button'] = "Voltar"
		context['back_link'] = reverse_lazy("login")
		context['form_button'] = "Enviar"
		context['form_button_class'] = "success"
		context['editable'] = True

		params = {"template_name": "configuration/recover_password.html",
			"password_reset_form": PasswordRecoverForm,
			"email_template_name": "configuration/recover_password_email.html",
			"post_reset_redirect": reverse_lazy("configuration:recover_password_done"),
		}
		template_response = auth_views.password_reset(request, extra_context=context, **params)

		return template_response

	def dispatch(self, *args, **kwargs):
		return super(PasswordRecoverView, self).dispatch(*args, **kwargs)

class PasswordRecoverDoneView(RedirectView):
	url = reverse_lazy("login")

	permanent = False

	def get_redirect_url(self, *args, **kwargs):
		messages.success(self.request, 'Em instantes você receberá um e-mail com instruções de como prosseguir.')

		return super(PasswordRecoverDoneView, self).get_redirect_url(*args, **kwargs)

	def dispatch(self, *args, **kwargs):
		return super(PasswordRecoverDoneView, self).dispatch(*args, **kwargs)

class PasswordResetView(FormView):
	def reset_password(self, request, *args, **kwargs):
		context = super(PasswordResetView, self).get_context_data()
		context['page_title'] = 'Reconfigurar a senha'
		context['form_title'] = 'Reconfigurar a senha'
		context['action_link'] = reverse_lazy("configuration:reset_password", kwargs=kwargs)
		context['form_button'] = "Enviar"
		context['form_button_class'] = "success"
		context['editable'] = True

		params = {"template_name": "configuration/reset_password.html",
			"set_password_form": PasswordResetForm,
			"uidb64": kwargs["uidb64"],
			"token": kwargs["token"],
			"post_reset_redirect": reverse_lazy("configuration:reset_password_done"),
		}
		template_response = auth_views.password_reset_confirm(request, extra_context=context, **params)

		return template_response

	def dispatch(self, *args, **kwargs):
		return super(PasswordResetView, self).dispatch(*args, **kwargs)

class PasswordResetDoneView(RedirectView):
	url = reverse_lazy("login")

	permanent = False

	def get_redirect_url(self, *args, **kwargs):
		messages.success(self.request, 'Sua senha foi reconfigurada com sucesso! Utilize sua nova senha para entrar no sistema.')

		return super(PasswordResetDoneView, self).get_redirect_url(*args, **kwargs)

	def dispatch(self, *args, **kwargs):
		return super(PasswordResetDoneView, self).dispatch(*args, **kwargs)