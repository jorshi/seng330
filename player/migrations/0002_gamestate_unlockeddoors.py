# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameworld', '0001_initial'),
        ('player', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('current_room', models.OneToOneField(to='gameworld.Room')),
                ('player', models.OneToOneField(to='player.Player')),
            ],
        ),
        migrations.CreateModel(
            name='UnlockedDoors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('door', models.OneToOneField(to='gameworld.Door')),
                ('game_state', models.ForeignKey(to='player.GameState')),
            ],
        ),
    ]
