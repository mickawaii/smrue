# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smrue', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='measurement_unit',
            field=models.CharField(max_length=255, choices=[(b'w', b'W'), (b'kw', b'kW')]),
        ),
    ]
