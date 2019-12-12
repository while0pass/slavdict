# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-01 09:53


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0036_auto_20180816_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='part_of_speech',
            field=models.CharField(blank=True, choices=[(b'', b''), (b'a', '\u0441\u0443\u0449.'), (b'b', '\u043f\u0440\u0438\u043b.'), (b'c', '\u043c\u0435\u0441\u0442.'), (b'd', '\u0433\u043b.'), (b'e', '[\u043f\u0440\u0438\u0447.]'), (b'f', '\u043d\u0430\u0440\u0435\u0447.'), (b'g', '\u0441\u043e\u044e\u0437'), (b'h', '\u043f\u0440\u0435\u0434\u043b.'), (b'i', '\u0447\u0430\u0441\u0442.'), (b'j', '\u043c\u0435\u0436\u0434.'), (b'k', '[\u0447\u0438\u0441\u043b\u043e]'), (b'l', '[\u0431\u0443\u043a\u0432\u0430]'), (b'm', '\u043f\u0440\u0438\u0447.-\u043f\u0440\u0438\u043b.'), (b'n', '\u043f\u0440\u0435\u0434\u0438\u043a. \u043d\u0430\u0440\u0435\u0447.')], default=b'', max_length=1, verbose_name='\u0447\u0430\u0441\u0442\u044c \u0440\u0435\u0447\u0438'),
        ),
    ]
