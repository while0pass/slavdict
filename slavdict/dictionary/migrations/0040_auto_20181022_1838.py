# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-22 18:38


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0039_auto_20180930_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meaning',
            name='substantivus_csl',
            field=models.CharField(blank=True, default=b'', max_length=100, verbose_name='\u0446\u0441\u043b \u0444\u043e\u0440\u043c\u0430'),
        ),
    ]
