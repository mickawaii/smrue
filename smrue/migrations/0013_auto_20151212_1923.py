# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smrue', '0012_goal_value_absolute'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='measurement_unit',
            field=models.CharField(max_length=255, choices=[(b'W', b'w'), (b'kW', b'kw')]),
        ),
    ]
