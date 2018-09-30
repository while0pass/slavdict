# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-30 21:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0038_auto_20180928_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='special_case',
            field=models.CharField(blank=True, choices=[(b'', b''), (b'a', '\u041d\u0435\u0441\u043a\u043e\u043b\u044c\u043a\u043e \u043b\u0435\u043a\u0441\u0435\u043c \u043e\u0434\u043d\u043e\u0433\u043e \u0440\u043e\u0434\u0430'), (b'b', '2 \u043b\u0435\u043a\u0441\u0435\u043c\u044b, \u043c\u0443\u0436. \u0438 \u0436\u0435\u043d. \u0440\u043e\u0434\u0430'), (b'c', '2 \u043b\u0435\u043a\u0441\u0435\u043c\u044b, \u0441\u0440. \u0438 \u0436\u0435\u043d. \u0440\u043e\u0434\u0430'), (b'g', '2 \u043b\u0435\u043a\u0441\u0435\u043c\u044b, \u0436\u0435\u043d. \u0438 \u0441\u0440. \u0440\u043e\u0434\u0430'), (b'd', '2 \u043b\u0435\u043a\u0441\u0435\u043c\u044b, \u0436\u0435\u043d. \u0438 \u0442\u043e\u043b\u044c\u043a\u043e \u043c\u043d.'), (b'e', '2 \u043b\u0435\u043a\u0441\u0435\u043c\u044b, \u0442\u043e\u043b\u044c\u043a\u043e \u043c\u043d. \u0438 \u0436\u0435\u043d.'), (b'f', '3 \u043b\u0435\u043a\u0441\u0435\u043c\u044b, 3 \u043c\u0443\u0436. \u0438 \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0438\u0439 \u043d\u0435\u0438\u0437\u043c.'), (b'h', '4 \u043b\u0435\u043a\u0441\u0435\u043c\u044b [\u0432\u0438\u0445\u0440\u044c]'), (b'i', '\u0412\u044b\u043d\u0443\u0434\u0438\u0442\u044c \u043e\u0442\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u043f\u043e\u043c\u0435\u0442\u044b \xab\u043d\u0435\u043f\u0435\u0440\u0435\u0445. \u0438 \u043f\u0435\u0440\u0435\u0445.\xbb \u043f\u0440\u0438 \u0440\u0430\u0432\u043d\u043e\u043c \u043a\u043e\u043b-\u0432\u0435 \u043f\u0435\u0440\u0435\u0445. \u0438 \u043d\u0435\u043f\u0435\u0440\u0435\u0445. \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0439')], default='', max_length=1, verbose_name='\u0421\u0442\u0430\u0442\u044c\u044f \u043d\u0443\u0436\u0434\u0430\u0435\u0442\u0441\u044f \u0432 \u0441\u043f\u0435\u0446\u0438\u0430\u043b\u044c\u043d\u043e\u0439 \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0435'),
        ),
    ]
