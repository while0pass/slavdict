# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-23 20:54


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0026_remove_translation_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='translation',
            name='fragment_start',
            field=models.SmallIntegerField(blank=True, default=1, verbose_name='\u043d\u043e\u043c\u0435\u0440 \u0441\u043b\u043e\u0432\u0430 \u043d\u0430\u0447\u0430\u043b\u0430 \u0444\u0440\u0430\u0433\u043c\u0435\u043d\u0442\u0430'),
        ),
    ]
