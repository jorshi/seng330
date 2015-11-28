# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameworld', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usedecoration',
            name='item_change',
            field=models.ForeignKey(related_name='usedecoration_cause', to='gameworld.ItemUseState', null=True),
        ),
        migrations.AlterField(
            model_name='usepickupableitem',
            name='item_change',
            field=models.ForeignKey(related_name='usepickupableitem_cause', to='gameworld.ItemUseState', null=True),
        ),
    ]
