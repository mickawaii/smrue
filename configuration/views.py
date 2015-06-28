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

from sensor.models import Sensor
from equipment.models import Equipment
from configuration.models import Profile
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate, login, logout
from configuration.forms import ConfigForm, UserSetupForm
import json
from django.shortcuts import get_object_or_404
from django.db import transaction

class ConfigView(TemplateView):
	template_name = 'configuration/config.html'

	def get_context_data(self, **kwargs):
		context = super(ConfigView, self).get_context_data(**kwargs)

		context['page_title'] = 'Minhas configurações'

		context['action_link'] = reverse_lazy("configuration:config")

		context['form'] = ConfigForm()

		context['equipments'] = Equipment.objects.all()

		context['free_sensors'] = Sensor.objects.filter(equipment_id__isnull=True)

		return context

	def post(self, request):
		equipments = json.loads(request.POST["equipments"])
		income_type = request.POST["income_type"]

		with transaction.atomic():
			for obj in equipments:
				equipment = get_object_or_404(Equipment, pk=obj["equipment"])
				already_has_sensor = Sensor.objects.filter(equipment_id=obj["equipment"]).count()

				if obj["sensor"]:
					sensor = get_object_or_404(Sensor, pk=obj["sensor"])
					sensor.equipment = equipment
					sensor.save()
				elif already_has_sensor:
					sensor = equipment.sensor
					sensor.equipment_id = None
					sensor.save()

		return HttpResponseRedirect(reverse_lazy("configuration:config"))

	# @method_decorator(login_required(login_url=reverse_lazy('google_login:login_page')))
	def dispatch(self, *args, **kwargs):
		return super(ConfigView, self).dispatch(*args, **kwargs)

class UserView(CreateView):
	template_name = 'configuration/user.html'

	model = User

	form_class = UserSetupForm

	success_url = reverse_lazy("home") # Url para redirecionamento

	def get_context_data(self, **kwargs):
		context = super(UserView, self).get_context_data(**kwargs)

		context['page_title'] = 'Registro de Usuário'

		context['form_title'] = 'Registro de Usuário'

		context['action_link'] = reverse_lazy("configuration:user")

		context['form_button'] = "Salvar"
		context['form_button_class'] = "success"

		context['editable'] = True

		return context

	def form_valid(self, form):
		user = form.save()
		income_type = form.cleaned_data["income_type"]
		username = form['username'].value()
		password = form['password1'].value()

		if income_type:
			Profile.objects.create(user=user,income_type=income_type)

		user = authenticate(username=username, password=password)
		login(self.request, user)

		return HttpResponseRedirect(reverse("configuration:home"))

	def dispatch(self, *args, **kwargs):
		return super(UserView, self).dispatch(*args, **kwargs)
