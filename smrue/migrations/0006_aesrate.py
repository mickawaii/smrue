# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smrue', '0005_auto_20150618_2150'),
    ]

    operations = [
        migrations.CreateModel(
            name='AESRate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.DecimalField(verbose_name=b'Taxa de Convers\xc3\xa3o', editable=False, max_digits=4, decimal_places=2)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('range_start', models.DecimalField(verbose_name=b'Consumo m\xc3\xadnimo', editable=False, max_digits=4, decimal_places=2)),
                ('range_end', models.DecimalField(verbose_name=b'Consumo m\xc3\xa1ximo', editable=False, max_digits=4, decimal_places=2)),
            ],
        ),
    ]
