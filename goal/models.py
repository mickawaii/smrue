# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
from consumption.models import Consumption
import decimal

class Goal(models.Model):

	name = models.CharField(max_length=255)
	value_in_percent = models.DecimalField(
				max_digits=4, 
				decimal_places=2,
				default=50,
				validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ])
	value_absolute = models.DecimalField(
				default=0,
				decimal_places=2,
				max_digits=20
		)
	yearmonth_start = models.DateField('Começo')
	yearmonth_end = models.DateField('Fim')
	equipment = models.ForeignKey('Equipment', null=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "%s" % (self.name)

	class Meta:
		app_label = 'smrue'

	def save(self, force_insert=False, force_update=False):
		qs = Consumption.objects.values('moment', 'current', 'voltage').filter(moment__month=datetime.now().month, equipment=self.equipment)
		self.value_absolute = self.value_in_percent * decimal.Decimal(sum(map(lambda set: 
			set['voltage'] * set['current'], 
			qs
		)) / 100)
		super(Goal, self).save(force_insert, force_update)