# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameworld', '0002_auto_20151108_0257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='default_items',
            field=models.ManyToManyField(related_name='found_in', to='gameworld.FixedItem'),
        ),
    ]
