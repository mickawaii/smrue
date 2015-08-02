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

	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)

		context['page_title'] = 'AES Eletropaulo'

		context['list_title'] = 'AES Eletropaulo'

		context['']

		return context

	def refresh_rates(self, request):
		aes_link = "https://www.aeseletropaulo.com.br/para-sua-casa/prazos-e-tarifas/conteudo/tarifa-de-energia-eletrica"
		red_flag = "bandeira-vermelha"
		yellow_flag = "bandeira-amarela"
		green_flag = "bandeira-verde"
		valid_flags = [red_flag, yellow_flag, green_flag]

		# the worker will get all the groups from aes_link up to last_group_initial
		group_initials = ["B1", "B2", "B3"]

		f = urllib.urlopen(aes_link)
		s = f.read()
		f.close()

		soup = BeautifulSoup(s, "html.parser")

		flag_container = soup.find(attrs={ "class":"bandeira-tarifaria-bandeira" })
		flag_container_classes = flag_container["class"]
		flag_container_classes.remove("bandeira-tarifaria-bandeira")
		flag_color = flag_container_classes[0]

		if not flag_color in valid_flags:
			raise Exception("No corresponding flag color")

		table = soup.find(attrs={"class":"bandeira-tarifa"})
		group = soup.find(attrs={"class":"bandeira-esquerda"})

		with transaction.atomic():
			while group.findNext(attrs={"class":"bandeira-esquerda"}):
				is_sub_class = "no-break" in group["class"]
				has_sub_class = "no-break" in group.findNext(attrs={"class":"bandeira-esquerda"})["class"]

				if not is_sub_class:
					group_name = group.text

				if group_name[:2] in group_initials:
					aes_rate = {'range_start': None, 'range_end': None}

					if is_sub_class:
						aes_rate["name"] = group_name
						limits = re.findall("\d+", group.text)

						if len(limits) == 1:

							if re.search("superior", group.text):
								aes_rate["range_start"] = int(limits[0])
							else:
								aes_rate["range_end"] = int(limits[0])
						else:
							aes_rate["range_start"] = int(limits[0])
							aes_rate["range_end"] = int(limits[1])
							
						aes_rate["tusd"] = float(group.findNext("td").text.replace(",","."))
						aes_rate["te"] = float(group.findNext(attrs={"class": flag_color}).text.replace(",","."))

					elif not has_sub_class:
						aes_rate["name"] = group_name
						aes_rate["tusd"] = float(group.findNext("td").text.replace(",","."))
						aes_rate["te"] = float(group.findNext(attrs={"class": flag_color}).text.replace(",","."))

					if aes_rate.get("name", None):
						AESRate.objects.update_or_create(name=aes_rate["name"], range_start=aes_rate["range_start"], range_end=aes_rate["range_end"], defaults=aes_rate)
					
				group = group.findNext(attrs={"class":"bandeira-esquerda"})


		return HttpResponseRedirect(reverse_lazy('aes_rate:table'))

	def dispatch(self, *args, **kwargs):
		return super(IndexView, self).dispatch(*args, **kwargs)
