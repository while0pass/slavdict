# Generated by Django 2.2.12 on 2020-05-31 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0060_auto_20200521_1134'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tip',
            options={'ordering': ('ref',), 'verbose_name': 'подсказка для поля ввода', 'verbose_name_plural': 'подсказки для полей ввода'},
        ),
        migrations.AlterField(
            model_name='tip',
            name='ref',
            field=models.CharField(choices=[('Collocation.civil_equivalent', 'Collocation.civil_equivalent'), ('Collocation.collocation', 'Collocation.collocation'), ('CollocationGroup.additional_info', 'CollocationGroup.additional_info'), ('CollocationGroup.hidden', 'CollocationGroup.hidden'), ('CollocationGroup.phraseological', 'CollocationGroup.phraseological'), ('Entry.additional_info', 'Entry.additional_info'), ('Entry.antconc_query', 'Entry.antconc_query'), ('Entry.canonical_name', 'Entry.canonical_name'), ('Entry.civil_equivalent', 'Entry.civil_equivalent'), ('Entry.comparative', 'Entry.comparative'), ('Entry.gender', 'Entry.gender'), ('Entry.genitive', 'Entry.genitive'), ('Entry.hidden', 'Entry.hidden'), ('Entry.homonym_gloss', 'Entry.homonym_gloss'), ('Entry.homonym_order', 'Entry.homonym_order'), ('Entry.nom_sg', 'Entry.nom_sg'), ('Entry.onym', 'Entry.onym'), ('Entry.part_of_speech', 'Entry.part_of_speech'), ('Entry.participle_type', 'Entry.participle_type'), ('Entry.possessive', 'Entry.possessive'), ('Entry.sg1', 'Entry.sg1'), ('Entry.sg2', 'Entry.sg2'), ('Entry.short_form', 'Entry.short_form'), ('Entry.special_case', 'Entry.special_case'), ('Entry.tantum', 'Entry.tantum'), ('Entry.transitivity', 'Entry.transitivity'), ('Entry.uninflected', 'Entry.uninflected'), ('Etymology.additional_info', 'Etymology.additional_info'), ('Etymology.gloss', 'Etymology.gloss'), ('Etymology.language', 'Etymology.language'), ('Etymology.mark', 'Etymology.mark'), ('Etymology.meaning', 'Etymology.meaning'), ('Etymology.questionable', 'Etymology.questionable'), ('Etymology.source', 'Etymology.source'), ('Etymology.text', 'Etymology.text'), ('Etymology.translit', 'Etymology.translit'), ('Etymology.unclear', 'Etymology.unclear'), ('Etymology.unitext', 'Etymology.unitext'), ('Example.additional_info', 'Example.additional_info'), ('Example.address_text', 'Example.address_text'), ('Example.context', 'Example.context'), ('Example.example', 'Example.example'), ('Example.greek_eq_status', 'Example.greek_eq_status'), ('Example.note', 'Example.note'), ('GreekEquivalentForExample.additional_info', 'GreekEquivalentForExample.additional_info'), ('GreekEquivalentForExample.aliud', 'GreekEquivalentForExample.aliud'), ('GreekEquivalentForExample.initial_form', 'GreekEquivalentForExample.initial_form'), ('GreekEquivalentForExample.initial_form_phraseology', 'GreekEquivalentForExample.initial_form_phraseology'), ('GreekEquivalentForExample.mark', 'GreekEquivalentForExample.mark'), ('GreekEquivalentForExample.note', 'GreekEquivalentForExample.note'), ('GreekEquivalentForExample.order', 'GreekEquivalentForExample.order'), ('GreekEquivalentForExample.position', 'GreekEquivalentForExample.position'), ('GreekEquivalentForExample.source', 'GreekEquivalentForExample.source'), ('GreekEquivalentForExample.unitext', 'GreekEquivalentForExample.unitext'), ('Meaning.additional_info', 'Meaning.additional_info'), ('Meaning.figurative', 'Meaning.figurative'), ('Meaning.gloss', 'Meaning.gloss'), ('Meaning.hidden', 'Meaning.hidden'), ('Meaning.is_valency', 'Meaning.is_valency'), ('Meaning.meaning', 'Meaning.meaning'), ('Meaning.metaphorical', 'Meaning.metaphorical'), ('Meaning.special_case', 'Meaning.special_case'), ('Meaning.substantivus', 'Meaning.substantivus'), ('Meaning.substantivus_csl', 'Meaning.substantivus_csl'), ('Meaning.substantivus_type', 'Meaning.substantivus_type'), ('Meaning.transitivity', 'Meaning.transitivity'), ('MeaningContext.context', 'MeaningContext.context'), ('MeaningContext.left_text', 'MeaningContext.left_text'), ('MeaningContext.right_text', 'MeaningContext.right_text'), ('OrthographicVariant.idem', 'OrthographicVariant.idem'), ('OrthographicVariant.no_ref_entry', 'OrthographicVariant.no_ref_entry'), ('OrthographicVariant.order', 'OrthographicVariant.order'), ('OrthographicVariant.questionable', 'OrthographicVariant.questionable'), ('OrthographicVariant.reconstructed', 'OrthographicVariant.reconstructed'), ('OrthographicVariant.untitled_exists', 'OrthographicVariant.untitled_exists'), ('OrthographicVariant.use', 'OrthographicVariant.use'), ('OrthographicVariant.without_accent', 'OrthographicVariant.without_accent'), ('Participle.idem', 'Participle.idem'), ('Participle.order', 'Participle.order'), ('Participle.tp', 'Participle.tp'), ('Translation.additional_info', 'Translation.additional_info'), ('Translation.fragment_end', 'Translation.fragment_end'), ('Translation.fragment_start', 'Translation.fragment_start'), ('Translation.fragmented', 'Translation.fragmented'), ('Translation.hidden', 'Translation.hidden'), ('Translation.order', 'Translation.order'), ('Translation.source', 'Translation.source'), ('Translation.translation', 'Translation.translation')], max_length=50, primary_key=True, serialize=False, verbose_name='поле, к которому относится подсказка'),
        ),
        migrations.AlterField(
            model_name='tip',
            name='text',
            field=models.TextField(help_text='\n\n    <p style="font-size: xx-small; margin-bottom: 1em">\n    Для курсива, ссылок и абзацев используйте\n    <a target="_blank" href="https://docs.google.com/document/d/1onDgE9wkZSGbXZg5V3GdoPx8gQ4fhXe73E7Sn0qvDY4">разметку Markdown</a>.\n    В качестве предпросмотра используйте\n    <a target="_blank" href="https://markdownlivepreview.com/">Markdown\n    Live Preview</a>.</p>\n\n', verbose_name='подсказка для поля ввода'),
        ),
    ]