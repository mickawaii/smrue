# -*- coding: utf-8 -*-
from django.db import models

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

	def __unicode__(self):	
		return "%s" % (self.name)

	class Meta:
		app_label = 'smrue'