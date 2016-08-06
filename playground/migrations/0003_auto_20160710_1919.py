# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-10 19:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0002_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='reviewed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='answered_questions',
            field=models.ManyToManyField(blank=True, to='playground.Question'),
        ),
    ]