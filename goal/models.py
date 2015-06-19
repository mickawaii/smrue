# -*- coding: utf-8 -*-
from django.db import models

class Goal(models.Model):
	MEASUREMENT_UNITS = (("w", "W"), ("kw", "kW"))

	name = models.CharField(max_length=255)
	value_in_percent = models.DecimalField(max_digits=4, decimal_places=2)
	yearmonth_start = models.DateField('Começo')
	yearmonth_end = models.DateField('Fim')
	# nominal_power = models.FloatField(blank=True, null=True)
	# approximated_consumption = models.FloatField(blank=True, null=True)
	# measurement_unit = models.CharField(max_length=255, choices=MEASUREMENT_UNITS)
	# description = models.TextField(blank=True, null=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "%s" % (self.name)

	class Meta:
		app_label = 'smrue'
