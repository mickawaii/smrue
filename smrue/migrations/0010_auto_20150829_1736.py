# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smrue', '0009_auto_20150801_2053'),
    ]

    operations = [
        migrations.AddField(
            model_name='aesrate',
            name='flag_additional_tax',
            field=models.DecimalField(null=True, max_digits=11, decimal_places=6, blank=True),
        ),
        migrations.AddField(
            model_name='aesrate',
            name='valid_date',
            field=models.DateField(null=True),
        ),
    ]
