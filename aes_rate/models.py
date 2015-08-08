# -*- coding: utf-8 -*-
from django.db import models
from bs4 import BeautifulSoup
from django.db import transaction
import urllib
import re

class AESRate(models.Model):
	name = models.CharField(max_length=255, blank=True, null=True)
	# tarifa do uso de sistema de distribuicao
	tusd = models.DecimalField(max_digits=11, decimal_places=6, blank=True, null=True)
	# tarifa de energia
	te = models.DecimalField(max_digits=11, decimal_places=6, blank=True, null=True)
	# In kWh
	range_start = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
	range_end = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

	date = models.DateTimeField(auto_now_add=True)

	TAX_LINK = "https://www.aeseletropaulo.com.br/para-sua-casa/prazos-e-tarifas/conteudo/tarifa-de-energia-eletrica"

	def __unicode__(self):	
		return "%s" % (self.name)

	class Meta:
		app_label = 'smrue'

	def range_display(self):
		if self.range_start and self.range_end:
			display = "%d kW até %d kW" % (self.range_start, self.range_end)
		elif self.range_start:
			display = "a partir de %d kW" % (self.range_start)
		elif self.range_end:
			display = "até %d kW" % (self.range_end)
		else:
			display = "qualquer consumo"

		return display

	@staticmethod
	def update_info():
		# the worker will get all the groups from aes_link up to last_group_initial
		group_initials = ["B1", "B2", "B3"]

		f = urllib.urlopen(AESRate.TAX_LINK)
		s = f.read()
		f.close()

		soup = BeautifulSoup(s, "html.parser")

		table = soup.find(attrs={"class":"bandeira-tarifa"})
		group = table.find(attrs={"class":"bandeira-esquerda"})

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
						aes_rate["te"] = float(group.findNext("td").findNext("td").text.replace(",","."))

					elif not has_sub_class:
						aes_rate["name"] = group_name
						aes_rate["tusd"] = float(group.findNext("td").text.replace(",","."))
						aes_rate["te"] = float(group.findNext("td").findNext("td").text.replace(",","."))

					if aes_rate.get("name", None):
						AESRate.objects.update_or_create(name=aes_rate["name"], range_start=aes_rate["range_start"], range_end=aes_rate["range_end"], defaults=aes_rate)
					
				group = group.findNext(attrs={"class":"bandeira-esquerda"})