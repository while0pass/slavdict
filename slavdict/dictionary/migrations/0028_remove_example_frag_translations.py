# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-23 21:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0027_auto_20180523_2054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='example',
            name='frag_translations',
        ),
    ]