# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractUseItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('use_message', models.TextField()),
                ('use_pattern', models.CharField(max_length=256, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='FixedItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=None, max_length=30)),
                ('pickupable', models.BooleanField(default=False)),
                ('default_state', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ItemUseState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.IntegerField()),
                ('examine', models.TextField()),
                ('hidden', models.BooleanField(default=False)),
                ('short_desc', models.CharField(default=None, max_length=256)),
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
            name='Door',
            fields=[
                ('fixeditem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='gameworld.FixedItem')),
                ('locked', models.BooleanField(default=False)),
            ],
            bases=('gameworld.fixeditem',),
        ),
        migrations.CreateModel(
            name='UseDecoration',
            fields=[
                ('abstractuseitem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='gameworld.AbstractUseItem')),
            ],
            bases=('gameworld.abstractuseitem',),
        ),
        migrations.CreateModel(
            name='UseKey',
            fields=[
                ('abstractuseitem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='gameworld.AbstractUseItem')),
                ('on_door', models.ForeignKey(to='gameworld.Door')),
            ],
            bases=('gameworld.abstractuseitem',),
        ),
        migrations.CreateModel(
            name='UsePickupableItem',
            fields=[
                ('abstractuseitem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='gameworld.AbstractUseItem')),
                ('consumed', models.BooleanField(default=False)),
            ],
            bases=('gameworld.abstractuseitem',),
        ),
        migrations.AddField(
            model_name='room',
            name='default_items',
            field=models.ManyToManyField(related_name='found_in', to='gameworld.FixedItem'),
        ),
        migrations.AddField(
            model_name='itemusestate',
            name='item',
            field=models.ForeignKey(related_name='states', to='gameworld.FixedItem'),
        ),
        migrations.AddField(
            model_name='abstractuseitem',
            name='item_change',
            field=models.ForeignKey(related_name='abstractuseitem_cause', to='gameworld.ItemUseState', null=True),
        ),
        migrations.AddField(
            model_name='abstractuseitem',
            name='item_use_state',
            field=models.ForeignKey(related_name='abstractuseitem_action', to='gameworld.ItemUseState'),
        ),
        migrations.AddField(
            model_name='usepickupableitem',
            name='on_item',
            field=models.ForeignKey(related_name='action_on_self', to='gameworld.ItemUseState', null=True),
        ),
        migrations.AddField(
            model_name='usepickupableitem',
            name='on_item_change',
            field=models.ForeignKey(related_name='indirect_cause', to='gameworld.ItemUseState', null=True),
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
