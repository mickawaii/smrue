# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

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
	yearmonth_start = models.DateField('Começo')
	yearmonth_end = models.DateField('Fim')
	equipment = models.ForeignKey('Equipment', null=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "%s" % (self.name)

	class Meta:
		app_label = 'smrue'
