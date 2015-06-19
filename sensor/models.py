from django.db import models
from equipment.models import Equipment

class Sensor(models.Model):
	name = models.CharField(max_length=255)
	code = models.CharField(max_length=255)

	equipment = models.OneToOneField(Equipment)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "%s - %s" % (self.code, self.name)

	class Meta:
		app_label = 'smrue'