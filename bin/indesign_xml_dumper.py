#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
Скрипт делает XML-выгрузку словарной базы для InDesign.

При необходимости сделать выборочную выгрузку скрипту допустимо передавать
номера статей в качестве аргументов. Каждый номер можно отделять от другого
пробелами, запятыми или запятыми с пробелами, например:

    SCRIPT 1177,123 89 945, 234
"""
import itertools
import os
import re
import sys

import django
from coffin.shortcuts import render_to_string

sys.path.append(os.path.abspath('/var/www/slavdict'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'slavdict.settings')
django.setup()

from slavdict.dictionary.models import Entry, ucs_convert
from slavdict.dictionary.models import sort_key1, sort_key2, resolve_titles

def in_first_volume(wordform):
    return wordform.lstrip(u' =')[:1].lower() in (u'а', u'б')

entries = []
lexemes = Entry.objects.all()
test_entries = None
if len(sys.argv) > 1:
    r = re.compile(r'\s*,\s*|\s+')
    s = u' '.join(sys.argv[1:]).strip(' ,')
    test_entries = [int(i) for i in r.split(s)]
if test_entries:
    lexemes = lexemes.filter(pk__in=test_entries)
lexemes = [e for e in lexemes if e.first_volume]

for lexeme in lexemes:

    wordform = lexeme.base_vars[0].idem
    reference = None
    entries.append((wordform, reference, lexeme))
    key = sort_key1(wordform)

    # Варианты
    for var in lexeme.orth_vars_refs[1:]:
        wordform = resolve_titles(var.idem)
        key2 = sort_key1(wordform)
        if key2 != key:
            reference = ucs_convert(wordform)
            entries.append((wordform, reference, lexeme))

    # Названия народов
    COMMA = ur',\s+'
    if lexeme.nom_sg:
        wordform = lexeme.nom_sg
        reference = lexeme.nom_sg_ucs_wax[1]
        for wordform, reference in zip(
                re.split(COMMA, wordform), re.split(COMMA, reference)):
            entries.append((wordform, reference, lexeme))

    # Краткие формы
    #if lexeme.short_form:
    #    wordform = lexeme.short_form
    #    reference = lexeme.short_form_ucs
    #    entries.append((wordform, reference, lexeme))

    # Причастия
    #for participle in lexeme.participles:
    #    wordform = participle.idem
    #    reference = participle.idem_ucs
    #    entries.append((wordform, reference, lexeme))

other_volumes = [e for e in Entry.objects.all() if not e.first_volume]
for lexeme in other_volumes:
    for participle in lexeme.participles:
        if participle.tp not in ('1', '2', '3', '4'):
            wordform = participle.idem
            if in_first_volume(wordform):
                reference = participle.idem_ucs
                entries.append((wordform, reference, lexeme))

def sort_key(x):
    wordform, _, lexeme = x
    return sort_key1(wordform), lexeme.homonym_order or 0, sort_key2(wordform)

entries = sorted(set(entries), key=sort_key)
final_entries = []
for key, group in itertools.groupby(entries, lambda x: x[:2]):
    wordform, reference = key
    if not in_first_volume(wordform):
        continue
    lst = list(group)
    if len(lst) < 2:
        wordform, reference, lexeme = lst[0]
        final_entries.append((reference, lexeme))
    else:
        if reference is None:  # Статьи не ссылочные
            for wordform, reference, lexeme in lst:
                final_entries.append((reference, lexeme))
        else:  # Статьи ссылочные
            lst = [x[2] for x in lst]
            if all(x.homonym_order for x in lst):
                lexeme = {
                    'is_reference': True,
                    'references': [
                        {'reference_ucs': lst[0].base_vars[0].idem_ucs,
                         'homonym_order': u',\u00a0'.join(
                                    str(i.homonym_order) for i in lst if i)
                        }
                    ],
                }
            else:
                lexeme = {
                    'is_reference': True,
                    'references': [
                        {'reference_ucs': x.base_vars[0].idem_ucs,
                         'homonym_order': x.homonym_order or None}
                        for x in lst],
                    }
            final_entries.append((reference, lexeme))

xml = render_to_string('indesign/slavdict.xml', {'entries': final_entries})
sys.stdout.write(xml.encode('utf-8'))
sys.exit(0)
