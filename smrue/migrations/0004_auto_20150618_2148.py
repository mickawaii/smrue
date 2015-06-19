# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smrue', '0003_goal'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='equipment_id',
            field=models.ForeignKey(to='smrue.Equipment', null=True),
        ),
        migrations.AlterField(
            model_name='goal',
            name='yearmonth_end',
            field=models.DateField(verbose_name=b'Fim'),
        ),
        migrations.AlterField(
            model_name='goal',
            name='yearmonth_start',
            field=models.DateField(verbose_name=b'Come\xc3\xa7o'),
        ),
    ]
