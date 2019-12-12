# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-23 18:59


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0023_squash'),
    ]

    operations = [
        migrations.AddField(
            model_name='example',
            name='frag_translations',
            field=models.SmallIntegerField(blank=True, default=0, verbose_name='\u043a\u043e\u043b-\u0432\u043e \u0447\u0430\u0441\u0442\u0438\u0447\u043d\u044b\u0445 \u043f\u0435\u0440\u0435\u0432\u043e\u0434\u043e\u0432 \u043f\u0440\u0438\u043c\u0435\u0440\u0430'),
        ),
        migrations.AddField(
            model_name='translation',
            name='fragment_end',
            field=models.SmallIntegerField(blank=True, default=1000, verbose_name='\u043d\u043e\u043c\u0435\u0440 \u0441\u043b\u043e\u0432\u0430 \u043a\u043e\u043d\u0446\u0430 \u0444\u0440\u0430\u0433\u043c\u0435\u043d\u0442\u0430'),
        ),
        migrations.AddField(
            model_name='translation',
            name='fragment_start',
            field=models.SmallIntegerField(blank=True, default=1000, verbose_name='\u043d\u043e\u043c\u0435\u0440 \u0441\u043b\u043e\u0432\u0430 \u043d\u0430\u0447\u0430\u043b\u0430 \u0444\u0440\u0430\u0433\u043c\u0435\u043d\u0442\u0430'),
        ),
        migrations.AddField(
            model_name='translation',
            name='fragmented',
            field=models.BooleanField(default=False, verbose_name='\u043f\u0435\u0440\u0435\u0432\u043e\u0434 \u0442\u043e\u043b\u044c\u043a\u043e \u0447\u0430\u0441\u0442\u0438 \u043f\u0440\u0438\u043c\u0435\u0440\u0430'),
        ),
    ]
