# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-15 18:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0007_auto_20160714_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='flagged',
            field=models.BooleanField(default=False, help_text='Question or answers are incorrect, should be hidden until fixed.'),
        ),
        migrations.AlterField(
            model_name='question',
            name='reviewed',
            field=models.BooleanField(default=False, help_text='full review of all fields is completed'),
        ),
        migrations.AlterField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='questions', to='playground.Tag'),
        ),
        migrations.AlterField(
            model_name='question',
            name='version',
            field=models.CharField(blank=True, choices=[('python-2.7', 'python-2.7'), ('python-3.5', 'python-3.5'), ('django-1.9', 'django-1.9')], max_length=10),
        ),
    ]
