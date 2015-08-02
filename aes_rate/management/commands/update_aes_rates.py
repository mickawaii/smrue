# -*- encoding:utf-8 -*-
from django.core.management.base import NoArgsCommand, CommandError 
from optparse import make_option
from aes_rate.models import AESRate
from bs4 import BeautifulSoup
from django.db import transaction
import urllib
import re

class Command(BaseCommand):
	aes_link = "https://www.aeseletropaulo.com.br/para-sua-casa/prazos-e-tarifas/conteudo/tarifa-de-energia-eletrica"

	help = 'Update AES rates from %s' % aes_link
	
	requires_system_checks = True

	can_import_settings = True

	def handle(self, *args, **options):
		red_flag = "bandeira-vermelha"
		yellow_flag = "bandeira-amarela"
		green_flag = "bandeira-verde"

		# the worker will get all the groups from aes_link up to last_group_initial
		group_initials = ["B1", "B2", "B3"]

		f = urllib.urlopen(self.aes_link)
		s = f.read()
		f.close()

		soup = BeautifulSoup(s, "html.parser")

		flag_container = soup.find(attrs={ "class":"bandeira-tarifaria-bandeira" })
		flag_container_classes = flag_container["class"]
		flag_container_classes.remove("bandeira-tarifaria-bandeira")
		flag_color = flag_container_classes[0]
		table = soup.find(attrs={"class":"bandeira-tarifa"})
		group = soup.find(attrs={"class":"bandeira-esquerda"})

		while group != None:
			is_sub_class = "no-break" in group["class"]
			has_sub_class = "no-break" in group.findNext(attrs={"class":"bandeira-esquerda"})["class"]

			if not is_sub_class:
				group_name = group.text

			if group_name[:2] in group_initials:
				aes_rate = AESRate()

				if is_sub_class:
					aes_rate.name = group_name
					limits = re.findall("\d+", group.text)

					if len(limits) == 1:

						if re.search("superior", group.text):
							print [limits[0], None]

						else:
							print [None, limits[0]]

					else:
						print limits
					print group.findNext("td").text
					print group.findNext(attrs={"class": flag_color}).text		

				elif not has_sub_class:
					print group_name
					print [None, None]
					print group.findNext("td").text
					print group.findNext(attrs={"class": flag_color}).text

			group = group.findNext(attrs={"class":"bandeira-esquerda"})