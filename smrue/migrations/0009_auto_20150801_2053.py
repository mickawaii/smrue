# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smrue', '0008_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aesrate',
            name='value',
        ),
        migrations.AddField(
            model_name='aesrate',
            name='name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='aesrate',
            name='te',
            field=models.DecimalField(null=True, max_digits=11, decimal_places=6, blank=True),
        ),
        migrations.AddField(
            model_name='aesrate',
            name='tusd',
            field=models.DecimalField(null=True, max_digits=11, decimal_places=6, blank=True),
        ),
        migrations.AlterField(
            model_name='aesrate',
            name='range_end',
            field=models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='aesrate',
            name='range_start',
            field=models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='income_type',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
