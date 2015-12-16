# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameworld', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UseKey',
            fields=[
                ('abstractuseitem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='gameworld.AbstractUseItem')),
                ('on_door', models.ForeignKey(to='gameworld.Door')),
            ],
            bases=('gameworld.abstractuseitem',),
        ),
    ]
