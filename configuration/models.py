from django.db import models
from equipment.models import Equipment
from django.contrib.auth.models import Group, User

class Profile(models.Model):
	INCOME_TYPE_CHOICES = (('residential','Residencial'),('rural','Rural'),('other_classes','Demais Classes'))

	user = models.OneToOneField(User, blank=True, null=True, related_name='profile')
	income_type = models.CharField(max_length=255, choices=INCOME_TYPE_CHOICES)

	def __unicode__(self):
		return "%s" % (self.user.username)

	class Meta:
		app_label = 'smrue'