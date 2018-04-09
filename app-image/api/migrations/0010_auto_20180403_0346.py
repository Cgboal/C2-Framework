# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-03 03:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20180403_0248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module',
            name='container',
        ),
        migrations.RemoveField(
            model_name='module',
            name='hash',
        ),
        migrations.AddField(
            model_name='module',
            name='image',
            field=models.TextField(default='alpine:latest', max_length=256, unique=True),
            preserve_default=False,
        ),
    ]