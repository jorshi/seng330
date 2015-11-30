# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameworld', '0002_usekey'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemusestate',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]
