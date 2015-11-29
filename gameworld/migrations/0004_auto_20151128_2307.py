# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameworld', '0003_auto_20151128_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemusestate',
            name='item',
            field=models.ForeignKey(related_name='states', to='gameworld.FixedItem'),
        ),
        migrations.AlterField(
            model_name='usepickupableitem',
            name='on_item',
            field=models.ForeignKey(related_name='action_on_self', to='gameworld.ItemUseState', null=True),
        ),
        migrations.AlterField(
            model_name='usepickupableitem',
            name='on_item_change',
            field=models.ForeignKey(related_name='indirect_cause', to='gameworld.ItemUseState', null=True),
        ),
    ]
