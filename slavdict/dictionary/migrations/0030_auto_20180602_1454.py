# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-02 14:54


from django.db import migrations

def move_untitled_exists_data(apps, schema_editor):
    Entry = apps.get_model('dictionary', 'Entry')
    OV = apps.get_model('dictionary', 'OrthographicVariant')
    for e in Entry.objects.all():
        if e.untitled_exists:
            ov = OV.objects \
                   .filter(entry_id=e.pk, parent_id__isnull=True) \
                   .order_by('order', 'id').first()
            ov.untitled_exists = e.untitled_exists
            ov.save()

class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0029_orthographicvariant_untitled_exists'),
    ]

    operations = [
        migrations.RunPython(move_untitled_exists_data),
    ]
