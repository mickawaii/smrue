from celery import task
from aes_rate.models import AESRate

@task()
def add():
	# 
	return 3