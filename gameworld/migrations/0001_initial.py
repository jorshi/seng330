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
                ('name', models.CharField(default=b'', max_length=30)),
                ('examine', models.TextField(default=b'')),
                ('hidden', models.BooleanField(default=False)),
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
        migrations.CreateModel(
            name='Door',
            fields=[
                ('fixeditem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='gameworld.FixedItem')),
                ('locked', models.BooleanField(default=False)),
                ('room_a', models.ForeignKey(related_name='room_a', to='gameworld.Room')),
                ('room_b', models.ForeignKey(related_name='room_b', to='gameworld.Room')),
            ],
            bases=('gameworld.fixeditem',),
        ),
        migrations.AddField(
            model_name='fixeditem',
            name='created_in',
            field=models.ForeignKey(to='gameworld.Room'),
        ),
    ]
