# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamestate', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemstate',
            name='hidden',
        ),
        migrations.RemoveField(
            model_name='itemstate',
            name='state',
        ),
        migrations.AlterField(
            model_name='itemstate',
            name='item',
            field=models.ForeignKey(to='gameworld.ItemUseState'),
        ),
    ]
