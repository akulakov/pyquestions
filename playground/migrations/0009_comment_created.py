# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-15 19:05
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0008_auto_20160715_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 7, 15, 19, 5, 37, 205881)),
            preserve_default=False,
        ),
    ]