# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-11-02 20:23


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csl_annotations', '0004_auto_20191102_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annotation',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u0432\u0440\u0435\u043c\u044f \u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u044f'),
        ),
    ]
