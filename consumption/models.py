from django.db import models

# Create your models here.
class Consumption(models.Model):
	moment = models.DateTimeField()
	current = models.FloatField()
	voltage = models.FloatField()

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.moment

	class Meta:
		app_label = 'smrue'