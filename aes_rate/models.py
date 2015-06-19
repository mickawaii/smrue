# -*- coding: utf-8 -*-
from django.db import models

class AESRate(models.Model):

	value = models.DecimalField('Taxa de Conversão', max_digits=4, decimal_places=2,editable=False)
	date = models.DateTimeField(auto_now_add=True, editable=False)
	range_start = models.DecimalField('Consumo mínimo', max_digits=4, decimal_places=2, editable=False)
	range_end = models.DecimalField('Consumo máximo', max_digits=4, decimal_places=2, editable=False)

	def __unicode__(self):
		return "%s" % (self.name)

	class Meta:
		app_label = 'smrue'
