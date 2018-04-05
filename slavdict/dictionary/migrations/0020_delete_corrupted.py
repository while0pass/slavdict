# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-13 14:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0019_order345'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='etymology',
            name='corrupted',
        ),
        migrations.RemoveField(
            model_name='greekequivalentforexample',
            name='corrupted',
        ),
        migrations.AlterField(
            model_name='entry',
            name='gender',
            field=models.CharField(blank=True, choices=[(b'm', '\u043c.'), (b'f', '\u0436.'), (b'n', '\u0441.'), (b'd', '\u043c. \u0438\xa0\u0436.')], default=b'', max_length=1, verbose_name='\u0440\u043e\u0434'),
        ),
        migrations.AlterField(
            model_name='meaning',
            name='special_case',
            field=models.CharField(blank=True, choices=[(b'', b''), ('\u0418\u043c\u0435\u043d\u0430', ((b'a', '\u043a\u0430\u043d\u043e\u043d\u0438\u0447.'), (b'h', '\u0438\u043c\u044f \u0441\u043e\u0431\u0441\u0442\u0432.'), (b'i', '\u0442\u043e\u043f\u043e\u043d\u0438\u043c'))), ('\u0427\u0430\u0441\u0442\u0438 \u0440\u0435\u0447\u0438', ((b'f', '\u043d\u0430\u0440\u0435\u0447.'), (b'b', '\u043f\u0440\u0435\u0434\u043b.'), (b'c', '\u0447\u0430\u0441\u0442.'), (b'g', '\u043c\u0435\u0436\u0434.'))), ('\u0424\u043e\u0440\u043c\u044b \u0441\u043b\u043e\u0432\u0430', ((b'd', '\u0434\u0430\u0442.'), (b'k', '\u043c\u043d.'), (b'e', '\u0442\u0432\u043e\u0440. \u0435\u0434. \u0432 \u0440\u043e\u043b\u0438 \u043d\u0430\u0440\u0435\u0447.'), (b'l', '\u0432 \u0440\u043e\u043b\u0438 \u043d\u0430\u0440\u0435\u0447.'))), ('\u0414\u0440\u0443\u0433\u043e\u0435', ((b'j', '\u043f\u0440\u0435\u0438\u043c\u0443\u0449.'),))], default=b'', max_length=1, verbose_name='\u043e\u0441\u043e\u0431\u044b\u0435 \u0441\u043b\u0443\u0447\u0430\u0438'),
        ),
    ]