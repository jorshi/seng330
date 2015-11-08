# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameworld', '__first__'),
        ('player', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoorState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('locked', models.BooleanField()),
                ('door', models.ForeignKey(to='gameworld.Door')),
            ],
        ),
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
        migrations.AddField(
            model_name='itemstate',
            name='room_state',
            field=models.ForeignKey(to='gamestate.RoomState'),
        ),
        migrations.AddField(
            model_name='doorstate',
            name='game_state',
            field=models.ForeignKey(to='gamestate.GameState'),
        ),
        migrations.AddField(
            model_name='doorstate',
            name='room_a',
            field=models.ForeignKey(related_name='unlocked_a', to='gameworld.Room'),
        ),
        migrations.AddField(
            model_name='doorstate',
            name='room_b',
            field=models.ForeignKey(related_name='unlocked_b', to='gameworld.Room'),
        ),
    ]
