# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamestate', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('game_state', models.OneToOneField(primary_key=True, serialize=False, to='gamestate.GameState')),
                ('rooms_unlocked', models.PositiveSmallIntegerField(default=0)),
                ('items_taken', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.RenameField(
            model_name='gamestate',
            old_name='items',
            new_name='inventory',
        ),
    ]
