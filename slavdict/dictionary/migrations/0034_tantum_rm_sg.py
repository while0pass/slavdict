# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-11 18:19


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0033_auto_20180611_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='tantum',
            field=models.CharField(blank=True, choices=[(b'd', '\u0442\u043e\u043b\u044c\u043a\u043e \u0434\u0432.'), (b'p', '\u0442\u043e\u043b\u044c\u043a\u043e \u043c\u043d.')], default=b'', max_length=1, verbose_name='\u0447\u0438\u0441\u043b\u043e'),
        ),
    ]
