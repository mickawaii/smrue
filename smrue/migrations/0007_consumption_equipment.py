# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smrue', '0006_aesrate'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumption',
            name='equipment',
            field=models.ForeignKey(to='smrue.Equipment', null=True),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='equipment',
            field=models.OneToOneField(null=True, blank=True, to='smrue.Equipment'),
        ),

    ]
