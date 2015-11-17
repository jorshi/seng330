# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameworld', '0003_auto_20151109_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='fixeditem',
            name='shortdesc',
            field=models.CharField(default=None, max_length=30),
        ),
    ]
