# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-02 14:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0028_remove_example_frag_translations'),
    ]

    operations = [
        migrations.AddField(
            model_name='orthographicvariant',
            name='untitled_exists',
            field=models.BooleanField(default=False, verbose_name='\u0412\u0430\u0440\u0438\u0430\u043d\u0442 \u0431\u0435\u0437 \u0442\u0438\u0442\u043b\u0430 \u043f\u0440\u0435\u0434\u0441\u0442\u0430\u0432\u043b\u0435\u043d \u0432 \u0442\u0435\u043a\u0441\u0442\u0430\u0445'),
        ),
    ]