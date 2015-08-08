# -*- encoding:utf-8 -*-

# Usado para encontrar urls
from django.core.urlresolvers import reverse, reverse_lazy

# Usado para verificar permissões
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

# Classes de views
from django.views.generic.list import ListView
from django.http import HttpResponse, HttpResponseRedirect

from aes_rate.models import AESRate
from bs4 import BeautifulSoup
from django.db import transaction
import urllib
import re

class IndexView(ListView):
	template_name = 'aes_rate/table.html'

	model = AESRate

	context_object_name = 'aes_table'

	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)

		context['page_title'] = 'AES Eletropaulo'

		context['list_title'] = 'AES Eletropaulo'

		context['last_update'] = AESRate.objects.latest("date").date

		context['aes_link'] = AESRate.TAX_LINK

		return context

	def refresh_rates(self, request):
		AESRate.update_info()

		return HttpResponseRedirect(reverse_lazy('aes_rate:table'))

	def dispatch(self, *args, **kwargs):
		return super(IndexView, self).dispatch(*args, **kwargs)
