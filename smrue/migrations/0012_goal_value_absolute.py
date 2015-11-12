# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smrue', '0011_auto_20150911_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='value_absolute',
            field=models.DecimalField(default=0, max_digits=20, decimal_places=2),
        ),
    ]
