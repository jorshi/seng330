# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameworld', '0002_auto_20151127_2045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fixeditem',
            name='hidden',
        ),
        migrations.AddField(
            model_name='itemusestate',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]
