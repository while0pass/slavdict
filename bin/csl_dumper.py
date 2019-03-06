#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
Скрипт делает выгрузку словарной базы для портала "Цсл язык сегодня"

При необходимости сделать выборочную выгрузку скрипту допустимо передавать
номера статей в качестве аргументов. Каждый номер можно отделять от другого
пробелами, запятыми или запятыми с пробелами, например:

    SCRIPT 1177,123 89 945, 234
"""
import collections
import itertools
import math
import os
import re
import shutil
import signal
import sys

import django
from django.template.loader import render_to_string

sys.path.append(os.path.abspath('/var/www/slavdict'))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'slavdict.settings')
django.setup()

from slavdict.dictionary.models import convert_for_index
from slavdict.dictionary.models import Entry
from slavdict.dictionary.models import resolve_titles
from slavdict.dictionary.models import sort_key1
from slavdict.dictionary.models import sort_key2
from slavdict.dictionary.models import ucs_convert
from slavdict.dictionary.models import VOLUME_LETTERS
from slavdict.dictionary.viewmodels import _json

OUTPUT_DIR = '../csl/.temp/slavdict_generated'
ENTRIES_DIR = OUTPUT_DIR + '/entries'
FULL_IX = OUTPUT_DIR + '/full_index'
PART_IX = OUTPUT_DIR + '/partial_index'
GRIX = OUTPUT_DIR + '/greek_index'
GRIX_REV = OUTPUT_DIR + '/greek_index_reverse'
dirs = (OUTPUT_DIR, ENTRIES_DIR, FULL_IX, PART_IX, GRIX, GRIX_REV)
IX_ROOT = '_ix'  # Имя файла с корнем индекса

URL_PATTERN = u'./словарь/статьи/%s'
OUTPUT_VOLUMES = (1, 2)
OUTPUT_VOLUMES_LETTERS = reduce(lambda x, y: x + y, (VOLUME_LETTERS[volume]
    for volume in OUTPUT_VOLUMES if volume in VOLUME_LETTERS), ())
HINTS_NUMBER = 7
PAGE_RESULTS_NUMBER = 30

def csl_url(entry):
    return URL_PATTERN % entry.id

CSI = '\033['
HIDE_CURSOR = CSI + '?25l'
SHOW_CURSOR = CSI + '?25h'
ERASE_LINE = CSI + '2K'
ERASE_LINEEND = CSI + '0K'

def interrupt_handler(signum, frame):
    print >> sys.stderr, SHOW_CURSOR
    sys.exit(0)

signal.signal(signal.SIGINT, interrupt_handler)

print >> sys.stderr, HIDE_CURSOR
note =  'Volumes: ' + u', '.join(str(volume) for volume in OUTPUT_VOLUMES) + '\n'
note += 'Letters: ' + u', '.join(letter for letter in OUTPUT_VOLUMES_LETTERS)
print >> sys.stderr, note.encode('utf-8')
print >> sys.stderr

def in_output_volumes(wordform):
    return wordform.lstrip(u' =')[:1].lower() in OUTPUT_VOLUMES_LETTERS

for directory in dirs:
    if os.path.exists(directory):
        shutil.rmtree(directory)

for directory in dirs:
    if not os.path.exists(directory):
        os.makedirs(directory)



entries1 = []
# Это список всех потенциально возможных статей для выбранных томов,
# ограниченных списком test_entries, если он задан.

lexemes = Entry.objects.all()
test_entries = None
if len(sys.argv) > 1:
    r = re.compile(r'\s*,\s*|\s+')
    s = u' '.join(sys.argv[1:]).strip(' ,')
    test_entries = [int(i) for i in r.split(s)]
if test_entries:
    print >> sys.stderr, 'Entries to dump:', u', '.join(str(i) for i in test_entries)
    lexemes = lexemes.filter(pk__in=test_entries)
else:
    print >> sys.stderr, 'Entries to dump: ALL for the selected volumes'
lexemes = [e for e in lexemes if e.volume(OUTPUT_VOLUMES)]
lexemes_n = len(lexemes)
print >> sys.stderr, 'Number of selected lexemes:', lexemes_n
print >> sys.stderr

for i, lexeme in enumerate(lexemes):

    wordform = lexeme.base_vars[0].idem
    reference = None
    entries1.append((wordform, reference, lexeme))
    key = sort_key1(wordform)

    # Разные ссылочные статьи в пределах выбранных томов

    # 1) Варианты заглавного слова
    for var in lexeme.orth_vars_refs[1:]:
        wordform = resolve_titles(var.idem)
        key2 = sort_key1(wordform)
        if key2 != key:
            reference = ucs_convert(wordform)
            entries1.append((wordform, reference, lexeme))

    # 2) Названия народов
    COMMA = ur',\s+'
    if lexeme.nom_sg:
        wordform = lexeme.nom_sg
        reference = lexeme.nom_sg_ucs_wax[1]
        for wordform, reference in zip(
                re.split(COMMA, wordform), re.split(COMMA, reference)):
            entries1.append((wordform, reference, lexeme))

    # 3) Краткие формы
    #if lexeme.short_form:
    #    wordform = lexeme.short_form
    #    reference = lexeme.short_form_ucs
    #    entries1.append((wordform, reference, lexeme))

    # 4) Причастия
    #for participle in lexeme.participles:
    #    wordform = participle.idem
    #    reference = participle.idem_ucs
    #    entries1.append((wordform, reference, lexeme))

    # 5) Особые случаи
    if lexeme.civil_equivalent == u'быти':
        wordform = u"бꙋ'дꙋчи"
        reference = ucs_convert(wordform)
        entries1.append((wordform, reference, lexeme))

    note = u'Отбор претендентов на вокабулы [ %s%% ] %s\r' % (
        int(round(i / float(lexemes_n) * 100)),
        lexeme.civil_equivalent + ERASE_LINEEND)
    sys.stderr.write(note.encode('utf-8'))



if not test_entries:
    # 6) Добавляем ссылочные статьи, которые будут присутствовать в выводимых
    # томах и ссылаться на какие-то статьи из других томов.
    other_volumes = [e for e in Entry.objects.all() if not e.volume(OUTPUT_VOLUMES)]
    other_volumes_n = len(other_volumes)
    for i, lexeme in enumerate(other_volumes):
        for participle in lexeme.participles:
            if participle.tp not in ('1', '2', '3', '4'):
                wordform = participle.idem
                if in_output_volumes(wordform):
                    reference = participle.idem_ucs
                    entries1.append((wordform, reference, lexeme))

        note = u'Поиск ссылок на другие тома [ %s%% ] %s\r' % (
            int(round(i / float(other_volumes_n) * 100)),
            lexeme.civil_equivalent + ERASE_LINEEND)
        sys.stderr.write(note.encode('utf-8'))

def sort_key(x):
    wordform, reference, lexeme = x
    if reference:
        ref_wordform = lexeme.base_vars[0].idem
        key = (sort_key1(wordform), -1, sort_key2(wordform),
               sort_key1(ref_wordform), lexeme.homonym_order or 0, sort_key2(ref_wordform))
    else:
        key = sort_key1(wordform), lexeme.homonym_order or 0, sort_key2(wordform)
    return key

note = u'Сортировка результатов...' + ERASE_LINEEND + '\r'
sys.stderr.write(note.encode('utf-8'))
entries1 = sorted(set(entries1), key=sort_key)
entries1_n = len(entries1)

entries2 = []
# Список статей, где ссылочные статьи сгруппированы по номеру омонима

for i, (key, group) in enumerate(itertools.groupby(entries1, lambda x: x[:2])):
    wordform, reference = key
    note = u'Группировка ссылочных статей [ %s%% ] %s\r' % (
        int(round(i / float(entries1_n) * 100)),
        wordform + ERASE_LINEEND)
    sys.stderr.write(note.encode('utf-8'))
    if not in_output_volumes(wordform):
        continue
    # Удаляем из выгрузки отсылочную статью Ассирии, т.к. она неправильно выгружается
    if wordform == u"ассѵрі'и":
        continue
    lst = list(group)
    if len(lst) < 2:
        wordform, reference, lexeme = lst[0]
        entries2.append((wordform, reference, lexeme))
    else:
        if reference is None:  # Статьи не ссылочные
            for wordform, reference, lexeme in lst:
                entries2.append((wordform, reference, lexeme))
        else:  # Статьи ссылочные
            lst = [x[2] for x in sorted(lst, key=sort_key)]
            lexeme = {
                'is_reference': True,
                'referenced_lexemes': lst,
            }
            if all(x.homonym_order for x in lst):
                lexeme['references'] = [
                            {'reference_ucs': lst[0].base_vars[0].idem_ucs,
                             'homonym_order': u',\u00a0'.join(
                                        str(i.homonym_order) for i in lst if i)
                            }]
            else:
                lexeme['references'] = [
                                    {'reference_ucs': x.base_vars[0].idem_ucs,
                                     'homonym_order': x.homonym_order or None}
                                    for x in lst],
            entries2.append((wordform, reference, lexeme))
entries2_n = len(entries2)


entries3 = []
# Список статей, в том числе ссылочных, но с устранением ссылок,
# расположенных вплотную к целевым статьям

for i, (wordform, reference, lexeme) in enumerate(entries2):
    note = u'Устранение ссылок, примыкающих к целевым статьям [ %s%% ]%s\r' % (
            int(round(i / float(entries2_n) * 100)), ERASE_LINEEND)
    sys.stderr.write(note.encode('utf-8'))
    checklist = set()
    for j in (i - 1, i + 1):
        if 0 <= j < len(entries2) and \
                not entries2[j][1] and not isinstance(entries2[j][2], dict):
            checklist.add(entries2[j][2].id)
    if isinstance(lexeme, Entry):
        in_checklist = lexeme.id in checklist
    elif isinstance(lexeme, dict):
        ids = [referenced_lexeme.id
               for referenced_lexeme in lexeme['referenced_lexemes']]
        in_checklist = len(ids) == 1 and ids[0] not in checklist
    if not reference or not in_checklist:
        entries3.append((wordform, reference, lexeme))

class Reference(unicode):
    def __new__(cls, string, homonym_order=None):
        instance = unicode.__new__(cls, string)
        instance.homonym_order = homonym_order
        return instance

# Объединение статей по начальным буквам
letter_parts = []
part_entries = []
letter = entries3[0][0].lstrip(u' =')[0].upper()
entries3_n = len(entries3)
for j, (wordform, group) in enumerate(itertools.groupby(entries3, lambda x: x[0])):
    note = u'Группировка статей по начальным буквам [ %s%% ]%s\r' % (
            int(round(j / float(entries3_n) * 100)), ERASE_LINEEND)
    sys.stderr.write(note.encode('utf-8'))
    lst = list(group)
    if wordform.lstrip(u' =')[0].upper() != letter:
        letter_parts.append((letter, part_entries))
        part_entries = []
        letter = wordform.lstrip(u' =')[0].upper()
    if len(lst) < 2:
        wordform, reference, lexeme = lst[0]
        part_entries.append((reference, lexeme))
    else:
        for i, (wordform, reference, lexeme) in enumerate(lst):
            if reference:
                reference = Reference(reference, homonym_order=i+1)
            else:
                lexeme.homonym_order = i + 1
            part_entries.append((reference, lexeme))
letter_parts.append((letter, part_entries))

# Вывод статей
for letter, entries in letter_parts:
    N = len(entries)
    for i, (reference, entry) in enumerate(entries):
        if not reference:
            note = u'Вывод статей на «%s» [ %s%% ] %s\r' % (letter,
                    int(round(i / float(N) * 100)),
                    entry.civil_equivalent + ERASE_LINEEND)
            sys.stderr.write(note.encode('utf-8'))
            html = render_to_string('csl/entry.html', { 'entry': entry,
                'csl_url': csl_url })
            filename = os.path.join(ENTRIES_DIR, u'%s.htm' % entry.id)
            with open(filename, 'wb') as f:
                f.write(html.encode('utf-8'))


# Подготовка указателей статей и греческих указателей

partial_index = {}
# Частичный указатель статей, который будет использоваться
# непосредственно для поиска и отображения мгновенных результатов.
# На каждую последовательность букв поискового запроса
# дает не более чем HINTS_NUMBER число статей. Представляет собой
# многоуровневый указатель.

KEY_HINTS = 'h'
KEY_INDEX = 'i'
KEY_POSTFIX = 'p'

KEY_ENTRY = 'e'
KEY_ENTRY_ID = 'i'
KEY_HOMONYM_GLOSS = 'g'
KEY_HOMONYM_ORDER = 'o'
KEY_PART_OF_SPEECH = 'p'
KEY_REFEREE = 'r'

full_index = collections.defaultdict(list)
# Полный указатель статей, который будет использоваться
# для многостраничного отображения всех возможных статей на текущий поисковый
# запрос, но непосредственно в портальном поиске задействован не будет.
# Является плоским указателем.

KEY_RESULTS = 'r'
KEY_NEXTPAGE = 'n'

# KEY_ENTRY, KEY_ENTRY_ID, KEY_HOMONYM_GLOSS, KEY_HOMONYM_ORDER,
# KEY_PART_OF_SPEECH, KEY_REFEREE
KEY_GREEK_MATCHES = 'h'

greek_index = {}
# Прямой и обратный греческие указатели. Оба -- полные многоуровневые
# указатели от цсл слов к греческим и в обратную сторону. Будут использоваться
# и для поиска и для многостраничного отображения информации.

# KEY_INDEX, KEY_POSTFIX
KEY_GREEK_RESULTS = 'r'

KEY_GREEK_CSL = 'c'
KEY_GREEK_GREEK = 'g'


def get_hint(entry):
    hint =  {
        KEY_ENTRY_ID: entry.id,  # id лексемы в базе
        KEY_ENTRY: entry.base_vars[0].idem_ucs,  # Заглавное слово
    }
    if entry.homonym_order:
        hint[KEY_HOMONYM_ORDER] = entry.homonym_order  # Номер омонима
        pos = entry.get_part_of_speech_display()  # Часть речи
        NON_PART_OF_SPEECH = pos.startswith(u'[')
        if not NON_PART_OF_SPEECH:
            hint[KEY_PART_OF_SPEECH] = pos
    if entry.homonym_gloss.strip():
        hint[KEY_HOMONYM_GLOSS] = entry.homonym_gloss.strip()  # Комментарий к омониму
    return hint

def get_reference_hint(reference, lexeme):
    hint = {
        KEY_ENTRY: reference,
    }
    if isinstance(lexeme, Entry):
        hint[KEY_REFEREE] = get_hint(lexeme)
    else:
        referenced_lexemes = lexeme['referenced_lexemes']
        referee_hint = get_hint(referenced_lexemes[0])
        if (len(referenced_lexemes) > 1
                and all(e.homonym_order for e in referenced_lexemes)):
            referee_hint[KEY_HOMONYM_ORDER] = u',\u00a0'.join(
                    str(e.homonym_order) for e in referenced_lexemes if e)
        hint[KEY_REFEREE] = referee_hint
    return hint

def get_greek(lexeme, hint):
    greeks = []
    if isinstance(lexeme, Entry):
        entries = [lexeme]
    else:
        entries = lexeme['referenced_lexemes']
    greeks = set()
    for e in entries:
        greeks.update(e.get_all_greeks())
    if len(greeks) == 0:
        return None
    hint[KEY_GREEK_MATCHES] = tuple(sorted(greeks))
    return hint

def already_in(hints, new_hint):
    for hint in hints:
        SAME_ENTRY = new_hint[KEY_ENTRY] == hint[KEY_ENTRY]
        SAME_HOMONYM = (KEY_HOMONYM_ORDER in new_hint
                and KEY_HOMONYM_ORDER in hint
                and new_hint[KEY_HOMONYM_ORDER] == hint[KEY_HOMONYM_ORDER])
        NON_HOMONYM = (KEY_HOMONYM_ORDER not in new_hint
                and KEY_HOMONYM_ORDER not in hint)
        if SAME_ENTRY and (SAME_HOMONYM or NON_HOMONYM):
            return True

# Создание индекса статей
for j, (wordform, reference, lexeme) in enumerate(entries2):
    slug = convert_for_index(wordform)
    ix_layer_pointer = partial_index

    note = u'Создание индекса статей [ %s%% ] %s\r' % (
            int(round(j / float(N) * 100)), slug + ERASE_LINEEND)
    sys.stderr.write(note.encode('utf-8'))

    if reference:
        hint = get_reference_hint(reference, lexeme)
    else:
        hint = get_hint(lexeme)
    for i, char in enumerate(slug):
        prefix = slug[:i + 1]
        if char not in ix_layer_pointer:
            ix_layer_pointer[char] = {
               KEY_INDEX: {},  # index: Следующий уровень индекса
               KEY_HINTS: [],  # hints: Первые N результатов,
            }                  # для подсказок при поиске
        hints = ix_layer_pointer[char][KEY_HINTS]
        if not already_in(hints, hint) and len(hints) < HINTS_NUMBER:
            hints.append(hint)
        results = full_index[prefix]
        if not already_in(results, hint):
            results.append(hint)
        ix_layer_pointer = ix_layer_pointer[char][KEY_INDEX]


def write_ix(filename, data):
    with open(filename, 'wb') as f:
        f.write(_json(data).encode('utf-8'))

def get_postfix(ix_layer):
    postfix = u''
    if len(ix_layer.keys()) > 0:
        first_key, first_value = list(ix_layer.items())[0]
        postfix = first_key + get_postfix(first_value[KEY_INDEX])
    return postfix

def no_change(node, attrname, N):
    if len(node) == 0:
        return True
    elif len(node) > 1:
        return False
    elif len(node) == 1:
        node_above = node[node.keys()[0]]
        if N != len(node_above[attrname]):
            return False
        return no_change(node_above[KEY_INDEX], attrname, N)

def decimal_to_base(decimal, base):
    digits = '0123456789abcdefghijklmnopqrstuvwxyz'
    result = ''
    while decimal != 0:
        result = digits[decimal % base] + result
        decimal /= base
    if result == '':
        result = '0'
    return result

def ixfn_convert(nodename):  # convert for index filenames
    return u''.join(decimal_to_base(ord(c), 36) for c in nodename)

# Вывод частичного указателя статей
def pix_tree_traversal(slug, ix_layer, hints):
    ix_node = {}
    hints_n = len(hints)
    if hints_n > 0:
        ix_node[KEY_HINTS] = hints
    if hints_n == 1 or no_change(ix_layer, KEY_HINTS, hints_n):
        postfix = get_postfix(ix_layer)
        if postfix:
            ix_node[KEY_POSTFIX] = postfix
    else:
        keys = u''.join(sorted(ix_layer.keys()))
        if keys:
            ix_node[KEY_INDEX] = keys
        for key, value in ix_layer.items():
            pix_tree_traversal(slug + key, value[KEY_INDEX], value[KEY_HINTS])

    note = u'Запись частичного индекса: %s%s\r' % (slug, ERASE_LINEEND)
    sys.stderr.write(note.encode('utf-8'))

    filename = os.path.join(
            PART_IX, '%s.json' % ixfn_convert(slug if slug else IX_ROOT))
    if os.path.exists(filename):
        note = u'Файл "%s" уже существует. Конфликт имен.%s\n' % (
                filename, ERASE_LINEEND)
        sys.stderr.write(note.encode('utf-8'))
    write_ix(filename, ix_node)

pix_tree_traversal('', partial_index, [])


# Вывод полного указателя статей
for key, value in full_index.items():
    if len(value) == 1:
        # Если список найденных результатов на запрос содержит всего одну
        # позицию, будет выводиться сразу единственная подходящая статья,
        # а выводить список смысла нету. Поэтому такие случаи в полный
        # указатель не включаем.
        continue
    data = {
        KEY_RESULTS: value[:PAGE_RESULTS_NUMBER],
    }
    if len(value) > PAGE_RESULTS_NUMBER:
        data[KEY_NEXTPAGE] = 1
    filename = os.path.join(FULL_IX, '%s.json' % ixfn_convert(key))
    if os.path.exists(filename):
        note = u'Файл "%s" уже существует. Конфликт имен.%s\n' % (
                filename, ERASE_LINEEND)
        sys.stderr.write(note.encode('utf-8'))
    write_ix(filename, data)
    pages_n = int(math.ceil(float(len(value)) / PAGE_RESULTS_NUMBER))
    for i in range(1, pages_n):
        data = {
            KEY_RESULTS: value[i*PAGE_RESULTS_NUMBER:(i+1)*PAGE_RESULTS_NUMBER],
        }
        if i < pages_n - 1:
            data[KEY_NEXTPAGE] = i + 1
        write_ix(filename + str(i), data)
    note = u'Запись полного индекса: %s%s\r' % (key, ERASE_LINEEND)
    sys.stderr.write(note.encode('utf-8'))


# Создание прямого греческого указателя
for j, (wordform, reference, lexeme) in enumerate(entries2):
    slug = convert_for_index(wordform)
    ix_layer_pointer = greek_index

    note = u'Создание прямого греч. индекса [ %s%% ] %s\r' % (
            int(round(j / float(N) * 100)), slug + ERASE_LINEEND)
    sys.stderr.write(note.encode('utf-8'))

    if reference:
        hint = get_reference_hint(reference, lexeme)
    else:
        hint = get_hint(lexeme)
    greek = get_greek(lexeme, hint)

    if greek:
        for i, char in enumerate(slug):
            prefix = slug[:i + 1]
            if char not in ix_layer_pointer:
                ix_layer_pointer[char] = {
                   KEY_INDEX: {},
                   KEY_GREEK_RESULTS: [],
                }
            greek_results = ix_layer_pointer[char][KEY_GREEK_RESULTS]
            if not already_in(greek_results, greek):
                greek_results.append(greek)
            ix_layer_pointer = ix_layer_pointer[char][KEY_INDEX]

# Вывод прямого греческого указателя
def grix_tree_traversal(slug, ix_layer, results):
    grix_node = {}
    N = len(results)
    if N > 0:
        grix_node[KEY_GREEK_RESULTS] = results[:PAGE_RESULTS_NUMBER]
    if N == 1 or no_change(ix_layer, KEY_GREEK_RESULTS, N):
        postfix = get_postfix(ix_layer)
        if postfix:
            grix_node[KEY_POSTFIX] = postfix
    else:
        keys = u''.join(sorted(ix_layer.keys()))
        if keys:
            grix_node[KEY_INDEX] = keys
        for key, value in ix_layer.items():
            grix_tree_traversal(slug + key,
                    value[KEY_INDEX], value[KEY_GREEK_RESULTS])

    note = u'Запись прямого греч. индекса: %s%s\r' % (slug, ERASE_LINEEND)
    sys.stderr.write(note.encode('utf-8'))

    filename = os.path.join(
            GRIX, '%s.json' % ixfn_convert(slug if slug else IX_ROOT))
    if os.path.exists(filename):
        note = u'Файл "%s" уже существует. Конфликт имен.%s\n' % (
                filename, ERASE_LINEEND)
        sys.stderr.write(note.encode('utf-8'))
    write_ix(filename, grix_node)

grix_tree_traversal('', greek_index, [])

sys.stderr.write(ERASE_LINE)
print >> sys.stderr, SHOW_CURSOR
sys.exit(0)
