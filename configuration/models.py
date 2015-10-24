from django.db import models
from equipment.models import Equipment
from aes_rate.models import AESRate
from django.contrib.auth.models import Group, User

class Profile(models.Model):
	user = models.OneToOneField(User, blank=True, null=True, related_name='profile')
	income_type = models.CharField(max_length=255, blank=True, null=True)

	def __unicode__(self):
		return "%s" % (self.user.username)

	class Meta:
		app_label = 'smrue'