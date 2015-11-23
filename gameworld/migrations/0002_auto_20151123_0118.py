# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameworld', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsePickupableItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('use_message', models.TextField()),
                ('use_pattern', models.CharField(max_length=200, blank=True)),
                ('on_item_change', models.IntegerField(null=True)),
                ('item_change', models.IntegerField(null=True)),
                ('consumed', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='useinventoryitem',
            name='item_use_state',
        ),
        migrations.RemoveField(
            model_name='useinventoryitem',
            name='on_item',
        ),
        migrations.RemoveField(
            model_name='itemusestate',
            name='alt_use_text',
        ),
        migrations.DeleteModel(
            name='UseInventoryItem',
        ),
        migrations.AddField(
            model_name='usepickupableitem',
            name='item_use_state',
            field=models.ForeignKey(to='gameworld.ItemUseState'),
        ),
        migrations.AddField(
            model_name='usepickupableitem',
            name='on_item',
            field=models.ForeignKey(to='gameworld.FixedItem', blank=True),
        ),
    ]
