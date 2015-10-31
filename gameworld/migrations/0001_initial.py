# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Door',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('locked', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='FixedItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('examine', models.TextField()),
                ('hidden', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=30)),
                ('desc_header', models.TextField()),
                ('desc_footer', models.TextField()),
                ('illuminated', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='fixeditem',
            name='created_in',
            field=models.ForeignKey(to='gameworld.Room'),
        ),
        migrations.AddField(
            model_name='door',
            name='room_a',
            field=models.ForeignKey(related_name='room_a', to='gameworld.Room'),
        ),
        migrations.AddField(
            model_name='door',
            name='room_b',
            field=models.ForeignKey(related_name='room_b', to='gameworld.Room'),
        ),
    ]
