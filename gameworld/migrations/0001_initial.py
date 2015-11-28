# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FixedItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=None, max_length=30)),
                ('hidden', models.BooleanField(default=False)),
                ('default_state', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ItemUseState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('examine', models.TextField()),
                ('short_desc', models.CharField(default=None, max_length=30)),
                ('state', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('name', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=50, blank=True)),
                ('desc_header', models.TextField(default=None)),
                ('desc_footer', models.TextField()),
                ('illuminated', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='UseDecoration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('use_message', models.TextField()),
                ('use_pattern', models.CharField(max_length=200, blank=True)),
                ('item_change', models.ForeignKey(related_name='usedecoration_cause', blank=True, to='gameworld.ItemUseState')),
                ('item_use_state', models.ForeignKey(related_name='usedecoration_action', to='gameworld.ItemUseState')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UsePickupableItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('use_message', models.TextField()),
                ('use_pattern', models.CharField(max_length=200, blank=True)),
                ('consumed', models.BooleanField(default=False)),
                ('item_change', models.ForeignKey(related_name='usepickupableitem_cause', blank=True, to='gameworld.ItemUseState')),
                ('item_use_state', models.ForeignKey(related_name='usepickupableitem_action', to='gameworld.ItemUseState')),
                ('on_item', models.ForeignKey(related_name='action_on_self', blank=True, to='gameworld.ItemUseState')),
                ('on_item_change', models.ForeignKey(related_name='indirect_cause', blank=True, to='gameworld.ItemUseState')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Door',
            fields=[
                ('fixeditem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='gameworld.FixedItem')),
                ('locked', models.BooleanField(default=False)),
            ],
            bases=('gameworld.fixeditem',),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('fixeditem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='gameworld.FixedItem')),
            ],
            bases=('gameworld.fixeditem',),
        ),
        migrations.AddField(
            model_name='room',
            name='default_items',
            field=models.ManyToManyField(related_name='found_in', to='gameworld.FixedItem'),
        ),
        migrations.AddField(
            model_name='itemusestate',
            name='item',
            field=models.ForeignKey(to='gameworld.FixedItem'),
        ),
        migrations.AddField(
            model_name='room',
            name='door_east',
            field=models.ForeignKey(related_name='east', blank=True, to='gameworld.Door', null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='door_north',
            field=models.ForeignKey(related_name='north', blank=True, to='gameworld.Door', null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='door_south',
            field=models.ForeignKey(related_name='south', blank=True, to='gameworld.Door', null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='door_west',
            field=models.ForeignKey(related_name='west', blank=True, to='gameworld.Door', null=True),
        ),
        migrations.AddField(
            model_name='door',
            name='room_a',
            field=models.ForeignKey(related_name='doors_a', to='gameworld.Room'),
        ),
        migrations.AddField(
            model_name='door',
            name='room_b',
            field=models.ForeignKey(related_name='doors_b', to='gameworld.Room'),
        ),
    ]
