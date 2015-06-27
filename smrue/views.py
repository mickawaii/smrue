# -*- encoding:utf-8 -*-

from django.views.generic.base import TemplateView, View
from django.conf import settings
from django.core.urlresolvers import reverse, reverse_lazy

from django.http.response import HttpResponse

import random
import string
import json

from collections import OrderedDict

class HomeView(TemplateView):
	template_name = 'home.html'

	def get_context_data(self, **kwargs):
		context = super(HomeView, self).get_context_data(**kwargs)

		context['page_title'] = 'SMRUE'

		context['config_user_link'] = reverse_lazy("configuration:user", kwargs={"user_pk": self.request.user.pk})

		return context