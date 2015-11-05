# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameworld', '0002_auto_20151104_1726'),
        ('player', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameState',
            fields=[
                ('player', models.OneToOneField(primary_key=True, serialize=False, to='player.Player')),
                ('current_room', models.ForeignKey(to='gameworld.Room')),
                ('items', models.ManyToManyField(to='gameworld.Item')),
            ],
        ),
        migrations.CreateModel(
            name='ItemState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hidden', models.BooleanField()),
                ('item', models.ForeignKey(to='gameworld.FixedItem')),
            ],
        ),
        migrations.CreateModel(
            name='RoomState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('illuminated', models.BooleanField()),
                ('game_state', models.ForeignKey(to='gamestate.GameState')),
                ('room', models.ForeignKey(to='gameworld.Room')),
            ],
        ),
        migrations.CreateModel(
            name='UnlockedDoors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('door', models.ForeignKey(to='gameworld.Door')),
                ('game_state', models.ForeignKey(to='gamestate.GameState')),
                ('room_a', models.ForeignKey(related_name='unlocked_a', to='gameworld.Room')),
                ('room_b', models.ForeignKey(related_name='unlocked_b', to='gameworld.Room')),
            ],
        ),
        migrations.AddField(
            model_name='itemstate',
            name='room_state',
            field=models.ForeignKey(to='gamestate.RoomState'),
        ),
    ]
