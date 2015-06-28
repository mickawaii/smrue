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

	@classmethod
	def new(cls, moment, current, voltage, equipment_id):
		c = cls(
			moment=moment, 
			current=current, 
			voltage=voltage, 
			equipment_id=equipment_id,
		)
		return c

	def __unicode__(self):
		return self.moment.strftime('%d-%m-%Y %H:%M')

	class Meta:
		app_label = 'smrue'