# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameworld', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UseDecoration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('keywords', models.CharField(max_length=200)),
                ('desc', models.TextField()),
                ('script', models.CharField(max_length=200, blank=True)),
                ('item', models.ForeignKey(to='gameworld.FixedItem')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UseInventoryItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('keywords', models.CharField(max_length=200)),
                ('desc', models.TextField()),
                ('script', models.CharField(max_length=200, blank=True)),
                ('item', models.ForeignKey(related_name='use_cases', to='gameworld.Item')),
                ('on_item', models.ForeignKey(to='gameworld.FixedItem', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='itemuse',
            name='item',
        ),
        migrations.RemoveField(
            model_name='itemuse',
            name='on_item',
        ),
        migrations.DeleteModel(
            name='ItemUse',
        ),
    ]
