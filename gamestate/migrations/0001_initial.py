# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameworld', '__first__'),
        ('player', '0001_initial'),
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
            ],
        ),
        migrations.CreateModel(
            name='ItemState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hidden', models.BooleanField()),
                ('state', models.IntegerField()),
                ('item', models.ForeignKey(to='gameworld.FixedItem')),
            ],
        ),
        migrations.CreateModel(
            name='RoomState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('illuminated', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('game_state', models.OneToOneField(primary_key=True, serialize=False, to='gamestate.GameState')),
                ('rooms_unlocked', models.PositiveSmallIntegerField(default=0)),
                ('items_taken', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='roomstate',
            name='game_state',
            field=models.ForeignKey(to='gamestate.GameState'),
        ),
        migrations.AddField(
            model_name='roomstate',
            name='room',
            field=models.ForeignKey(to='gameworld.Room'),
        ),
        migrations.AddField(
            model_name='itemstate',
            name='room_state',
            field=models.ForeignKey(to='gamestate.RoomState'),
        ),
        migrations.AddField(
            model_name='gamestate',
            name='current_room',
            field=models.ForeignKey(to='gameworld.Room'),
        ),
        migrations.AddField(
            model_name='gamestate',
            name='inventory',
            field=models.ManyToManyField(to='gameworld.Item'),
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
