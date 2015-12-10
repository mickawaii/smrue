from django.db import models

class Equipment(models.Model):
	MEASUREMENT_UNITS = (("W", "w"), ("kW", "kw"))

	name = models.CharField(max_length=255)
	nominal_power = models.FloatField(blank=True, null=True)
	approximated_consumption = models.FloatField(blank=True, null=True)
	measurement_unit = models.CharField(max_length=255, choices=MEASUREMENT_UNITS)
	description = models.TextField(blank=True, null=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "%s" % (self.name)

	class Meta:
		app_label = 'smrue'
