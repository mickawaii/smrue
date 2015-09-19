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
from django.db.models import Max
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

		context['last_update'] = AESRate.objects.order_by("-date").values_list("date",flat=True).first()

		context['aes_link'] = AESRate.TAX_LINK

		return context

	def get_queryset(self):
		queryset = super(IndexView, self).get_queryset()
		latest_date = queryset.aggregate(max_date=Max("valid_date"))["max_date"]
		if latest_date:
			year = latest_date.year
			month = latest_date.month
			day = latest_date.day

			queryset = queryset.filter(valid_date__year=year, valid_date__month=month, valid_date__day=day).order_by("name").order_by("-valid_date")

		return queryset

	def refresh_rates(self, request):
		AESRate.update_info()

		return HttpResponseRedirect(reverse_lazy('aes_rate:table'))

	def dispatch(self, *args, **kwargs):
		return super(IndexView, self).dispatch(*args, **kwargs)
