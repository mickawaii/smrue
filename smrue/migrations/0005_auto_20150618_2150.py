# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smrue', '0004_auto_20150618_2148'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goal',
            old_name='equipment_id',
            new_name='equipment',
        ),
    ]
