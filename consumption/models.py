from django.db import models
from equipment.models import Equipment

# Create your models here.
class Consumption(models.Model):
	moment = models.DateTimeField()
	current = models.FloatField()
	voltage = models.FloatField()
	equipment = models.ForeignKey(Equipment, null=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.moment

	class Meta:
		app_label = 'smrue'