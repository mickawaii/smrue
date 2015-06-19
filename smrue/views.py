from django.views.generic.base import TemplateView, View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.views.generic.detail import  DetailView
from django.views.generic.edit import FormView
from django.conf import settings
from django.core.paginator import Paginator

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

		return context
