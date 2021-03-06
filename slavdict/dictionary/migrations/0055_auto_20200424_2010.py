# Generated by Django 2.2.12 on 2020-04-24 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0054_remove_translation_is_synodal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='translation',
            name='source',
            field=models.CharField(choices=[('', ''), ('S', 'Синодальный перевод'), ('R', 'Перевод РБО'), ('A', 'Адаменко В., свящ.'), ('B', 'Бируковы'), ('G', '(Говоров) Феофан, еп. — перевод Добротолюбия'), ('K', 'Кедров Н. — перевод великого канона'), ('L', 'Ловягин Е.И. — перевод канонов'), ('2', 'Ловягин И.Ф. — перевод октоиха'), ('N', 'Нахимов Н. (Зайончковский Н.Ч.)'), ('P', '(Полянский) Иустин, еп. — перевод Алфавита духовного'), ('3', 'Седакова О.А.'), ('T', '(Тимрот) Амвросий, иером.'), ('J', 'Юнгеров П.А.')], default='', max_length=1, verbose_name='Источник'),
        ),
    ]
