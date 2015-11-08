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
                ('examine', models.TextField()),
                ('hidden', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ItemUse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('keywords', models.CharField(default=b'use', max_length=200)),
                ('use_message', models.TextField()),
                ('use_script', models.CharField(max_length=200, blank=True)),
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
            name='Item',
            fields=[
                ('fixeditem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='gameworld.FixedItem')),
            ],
            bases=('gameworld.fixeditem',),
        ),
        migrations.AddField(
            model_name='room',
            name='default_items',
            field=models.ManyToManyField(to='gameworld.FixedItem'),
        ),
        migrations.AddField(
            model_name='itemuse',
            name='use_on',
            field=models.ForeignKey(to='gameworld.FixedItem', blank=True),
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
            model_name='itemuse',
            name='item',
            field=models.ForeignKey(related_name='use_cases', to='gameworld.Item'),
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
