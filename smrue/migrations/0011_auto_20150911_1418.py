# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('smrue', '0010_auto_20150829_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aesrate',
            name='date',
            field=models.DateTimeField(auto_now_add=True, db_index=True, db_tablespace=b'pg_default'),
        ),
        migrations.AlterField(
            model_name='aesrate',
            name='flag_additional_tax',
            field=models.DecimalField(decimal_places=6, max_digits=11, db_tablespace=b'pg_default', blank=True, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='aesrate',
            name='name',
            field=models.CharField(db_index=True, max_length=255, null=True, db_tablespace=b'pg_default', blank=True),
        ),
        migrations.AlterField(
            model_name='aesrate',
            name='range_end',
            field=models.DecimalField(decimal_places=2, max_digits=8, db_tablespace=b'pg_default', blank=True, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='aesrate',
            name='range_start',
            field=models.DecimalField(decimal_places=2, max_digits=8, db_tablespace=b'pg_default', blank=True, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='aesrate',
            name='te',
            field=models.DecimalField(decimal_places=6, max_digits=11, db_tablespace=b'pg_default', blank=True, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='aesrate',
            name='tusd',
            field=models.DecimalField(decimal_places=6, max_digits=11, db_tablespace=b'pg_default', blank=True, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='aesrate',
            name='valid_date',
            field=models.DateField(null=True, db_tablespace=b'pg_default', db_index=True),
        ),
        migrations.AlterField(
            model_name='goal',
            name='value_in_percent',
            field=models.DecimalField(default=50, max_digits=4, decimal_places=2, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)]),
        ),
    ]
