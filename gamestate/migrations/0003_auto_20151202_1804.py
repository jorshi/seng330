# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamestate', '0002_remove_itemstate_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamestate',
            name='current_room',
            field=models.ForeignKey(to='gamestate.RoomState', null=True),
        ),
        migrations.AlterField(
            model_name='gamestate',
            name='inventory',
            field=models.ManyToManyField(to='gameworld.ItemUseState'),
        ),
    ]
