# -*- coding: utf-8 -*-

from dictionary.forms import BilletImportForm
from django.http import HttpResponse, HttpResponseRedirect
import slavdict.unicode_csv as unicode_csv
import StringIO

from custom_user.models import CustomUser
from slavdict.directory.models import CategoryValue
ccc = CategoryValue.objects.get(pk=46) # Импортирована (Статус статьи "Статья импортирована из Moodle")

from slavdict.dictionary.models import entry_dict


orthvars = []

csv_columns = {
    u'Заглавное слово': '',
    u'Отсылка': '',
    u'Орфографический вариант (1)': '',
    u'Орфографический вариант (2)': '',
    u'Орфографический вариант (3)': '',
    u'Орфографический вариант (4)': '',
    u'Часть речи': '',
    u'Словоформы': '',
    u'1 лицо': '',
    u'2 лицо': '',
    u'Р. падеж': '',
    u'Род': '',
    u'Число': '',
    u'Разряд по значению': '',
    u'Неизменяемость': '',
    u'Значение слова (1)': '',
    u'Значение слова (2)': '',
    u'Значение слова (3)': '',
    u'Значение слова (4)': '',
    u'Значение слова (5)': '',
    u'Пример для значения 1 (1)': '',
    u'Пример для значения 1 (2)': '',
    u'Пример для значения 1 (3)': '',
    u'Пример для значения 2 (1)': '',
    u'Пример для значения 2 (2)': '',
    u'Пример для значения 2 (3)': '',
    u'Пример для значения 3 (1)': '',
    u'Пример для значения 3 (2)': '',
    u'Пример для значения 3 (3)': '',
    u'Пример для значения 4 (1)': '',
    u'Пример для значения 4 (2)': '',
    u'Пример для значения 4 (3)': '',
    u'Пример для значения 5 (1)': '',
    u'Пример для значения 5 (2)': '',
    u'Пример для значения 5 (3)': '',
    u'Адрес для примера 1.1': '',
    u'Адрес для примера 1.2': '',
    u'Адрес для примера 1.3': '',
    u'Адрес для примера 2.1': '',
    u'Адрес для примера 2.2': '',
    u'Адрес для примера 2.3': '',
    u'Адрес для примера 3.1': '',
    u'Адрес для примера 3.2': '',
    u'Адрес для примера 3.3': '',
    u'Адрес для примера 4.1': '',
    u'Адрес для примера 4.2': '',
    u'Адрес для примера 4.3': '',
    u'Адрес для примера 5.1': '',
    u'Адрес для примера 5.2': '',
    u'Адрес для примера 5.3': '',
    u'Автор статьи': '',
    u'Запрос для AntConc': '',
    u'Греч. параллель для слав. слов': '',
    u'Виза редактора': '',
    u'Статус': '',
    u'Реконструкция': '',
    u'Наличие запроса для AntConc': '',
    u'Комментарий редактора': '',
    u'Свободное поле': '',
    u'Наличие замечаний редактора': '',
    u'Надежность реконструкции': '',
    u'Контекст 1.1': '',
    u'Контекст 1.2': '',
    u'И.ед. для ‘тот или иной народ’': '',
    u'Краткая форма': '',
    u'Имя собственное': '',
    u'Метафорическое употребление (1)': '',
    u'Устойчивое сочетание (3)': '',
    u'Устойчивое сочетание (1)': '',
    u'Устойчивое сочетание (2)': '',
    u'Греч. параллель': '',
    u'Контекст 1.3': '',
    u'Греч. параллель для контекста 1.1': '',
    u'Греч. параллель для контекста 1.2': '',
    u'Греч. параллель для контекста 1.3': '',
    u'Метафорическое употребление (2)': '',
    u'Метафорическое употребление (3)': '',
    u'Пример для метафоры 1.1': '',
    u'Пример для метафоры 1.2': '',
    u'Пример для метафоры 1.3': '',
    u'Пример для метафоры 2.1': '',
    u'Пример для метафоры 2.2': '',
    u'Пример для метафоры 2.3': '',
    u'Пример для метафоры 3.1': '',
    u'Пример для метафоры 3.2': '',
    u'Пример для метафоры 3.3': '',
    u'Адрес для примера метафоры 1.1': '',
    u'Адрес для примера метафоры 1.2': '',
    u'Адрес для примера метафоры 1.3': '',
    u'Адрес для примера метафоры 2.1': '',
    u'Адрес для примера метафоры 2.2': '',
    u'Адрес для примера метафоры 2.3': '',
    u'Адрес для примера метафоры 3.1': '',
    u'Адрес для примера метафоры 3.2': '',
    u'Адрес для примера метафоры 3.3': '',
    u'Наличие греч. параллелей для контекстов': '',
    u'Толкование слова (1)': '',
    u'Толкование слова (2)': '',
    u'Толкование слова (3)': '',
    u'Толкование слова (4)': '',
    u'Толкование слова (5)': '',
    u'Контекст 2.1': '',
    u'Контекст 2.2': '',
    u'Контекст 2.3': '',
    u'Контекст 3.1': '',
    u'Контекст 3.2': '',
    u'Контекст 3.3': '',
    u'Контекст 4.1': '',
    u'Контекст 4.2': '',
    u'Контекст 4.3': '',
    u'Контекст 5.1': '',
    u'Контекст 5.2': '',
    u'Контекст 5.3': '',
    u'Греч. параллель для контекста 2.1': '',
    u'Греч. параллель для контекста 2.2': '',
    u'Греч. параллель для контекста 2.3': '',
    u'Греч. параллель для контекста 3.1': '',
    u'Греч. параллель для контекста 3.2': '',
    u'Греч. параллель для контекста 3.3': '',
    u'Греч. параллель для контекста 4.1': '',
    u'Греч. параллель для контекста 4.2': '',
    u'Греч. параллель для контекста 4.3': '',
    u'Греч. параллель для контекста 5.1': '',
    u'Греч. параллель для контекста 5.2': '',
    u'Греч. параллель для контекста 5.3': '',
    u'Частотность': '',
    u'Контекст для метафоры 1.1': '',
    u'Контекст для метафоры 1.2': '',
    u'Контекст для метафоры 1.3': '',
    u'Контекст для метафоры 2.1': '',
    u'Контекст для метафоры 2.2': '',
    u'Контекст для метафоры 2.3': '',
    u'Контекст для метафоры 3.1': '',
    u'Контекст для метафоры 3.2': '',
    u'Контекст для метафоры 3.3': '',
    u'Греч. параллель для метафоры 1.1': '',
    u'Греч. параллель для метафоры 1.2': '',
    u'Греч. параллель для метафоры 1.3': '',
    u'Греч. параллель для метафоры 2.1': '',
    u'Греч. параллель для метафоры 2.2': '',
    u'Греч. параллель для метафоры 2.3': '',
    u'Греч. параллель для метафоры 3.1': '',
    u'Греч. параллель для метафоры 3.2': '',
    u'Греч. параллель для метафоры 3.3': '',
    u'Пример для значения 1 (4)': '',
    u'Пример для значения 1 (5)': '',
    u'Пример для значения 1 (6)': '',
    u'Пример для значения 1 (7)': '',
    u'Пример для значения 1 (8)': '',
    u'Адрес для примера 1.4': '',
    u'Адрес для примера 1.5': '',
    u'Адрес для примера 1.6': '',
    u'Адрес для примера 1.7': '',
    u'Адрес для примера 1.8': '',
    u'Греч. параллель для контекста 1.4': '',
    u'Греч. параллель для контекста 1.5': '',
    u'Греч. параллель для контекста 1.6': '',
    u'Греч. параллель для контекста 1.7': '',
    u'Греч. параллель для контекста 1.8': '',
    u'Контекст 1.4': '',
    u'Контекст 1.5': '',
    u'Контекст 1.6': '',
    u'Контекст 1.7': '',
    u'Контекст 1.8': '',
    u'Пример для значения 2 (4)': '',
    u'Адрес для примера 2.4': '',
    u'Контекст 2.4': '',
    u'Греч. параллель для контекста 2.4': '',
    u'Статус параллелей': '',
    u'Номер для словарных статей омонимов': '',
    u'Пояснение для словарных статей омонимов': '',
    u'Реконструкция орф. вар. (1)': '',
    u'Реконструкция орф. вар. (2)': '',
    u'Реконструкция орф. вар. (3)': '',
    u'Реконструкция орф. вар. (4)': '',
}

csv_translate = {
    'headword': u'Заглавное слово',
    'orthvar1': u'Орфографический вариант (1)',
    'orthvar2': u'Орфографический вариант (2)',
    'orthvar3': u'Орфографический вариант (3)',
    'orthvar4': u'Орфографический вариант (4)',
    
    'reconstr': u'Реконструкция',
    'reconstr_ov1': u'Реконструкция орф. вар. (1)',
    'reconstr_ov2': u'Реконструкция орф. вар. (2)',
    'reconstr_ov3': u'Реконструкция орф. вар. (3)',
    'reconstr_ov4': u'Реконструкция орф. вар. (4)',

    'reconstr_reliability': u'Надежность реконструкции',
    'frequency': u'Частотность',


    'hom_num': u'Номер для словарных статей омонимов',
    'hom_gloss': u'Пояснение для словарных статей омонимов',

    'etym': u'Греч. параллель',
    'etym0': u'Греч. параллель для слав. слов',

    'antconc': u'Запрос для AntConc',
    'antconc_bool': u'Наличие запроса для AntConc',
    'wordforms': u'Словоформы',

    'author': u'Автор статьи',
    'visa': u'Виза редактора',
    'status': u'Статус',
    'edcomment': u'Комментарий редактора',
    'edcomment_bool': u'Наличие замечаний редактора',
    'grequiv_status_bool': u'Наличие греч. параллелей для контекстов',
    'grequiv_status': u'Статус параллелей',

    'free': u'Свободное поле',

    'entry_sr': u'Отсылка',



    'pos': u'Часть речи',
    '1sg': u'1 лицо',
    '2sg': u'2 лицо',
    'Gen': u'Р. падеж',
    'NomSg': u'И.ед. для ‘тот или иной народ’',
    'gender': u'Род',
    'number': u'Число',
    'proper_name_type': u'Разряд по значению',
    'uninflected': u'Неизменяемость',
    'short_form': u'Краткая форма',
    'proper_name': u'Имя собственное',



    'm1': u'Значение слова (1)',
    'm2': u'Значение слова (2)',
    'm3': u'Значение слова (3)',
    'm4': u'Значение слова (4)',
    'm5': u'Значение слова (5)',

    'gl1': u'Толкование слова (1)',
    'gl2': u'Толкование слова (2)',
    'gl3': u'Толкование слова (3)',
    'gl4': u'Толкование слова (4)',
    'gl5': u'Толкование слова (5)',


    'm1ex1': u'Пример для значения 1 (1)',
    'm1ex2': u'Пример для значения 1 (2)',
    'm1ex3': u'Пример для значения 1 (3)',
    'm1ex4': u'Пример для значения 1 (4)',
    'm1ex5': u'Пример для значения 1 (5)',
    'm1ex6': u'Пример для значения 1 (6)',
    'm1ex7': u'Пример для значения 1 (7)',
    'm1ex8': u'Пример для значения 1 (8)',

    'm2ex1': u'Пример для значения 2 (1)',
    'm2ex2': u'Пример для значения 2 (2)',
    'm2ex3': u'Пример для значения 2 (3)',
    'm2ex4': u'Пример для значения 2 (4)',

    'm3ex1': u'Пример для значения 3 (1)',
    'm3ex2': u'Пример для значения 3 (2)',
    'm3ex3': u'Пример для значения 3 (3)',
    'm4ex1': u'Пример для значения 4 (1)',
    'm4ex2': u'Пример для значения 4 (2)',
    'm4ex3': u'Пример для значения 4 (3)',
    'm5ex1': u'Пример для значения 5 (1)',
    'm5ex2': u'Пример для значения 5 (2)',
    'm5ex3': u'Пример для значения 5 (3)',


    'm1adr1': u'Адрес для примера 1.1',
    'm1adr2': u'Адрес для примера 1.2',
    'm1adr3': u'Адрес для примера 1.3',
    'm1adr4': u'Адрес для примера 1.4',
    'm1adr5': u'Адрес для примера 1.5',
    'm1adr6': u'Адрес для примера 1.6',
    'm1adr7': u'Адрес для примера 1.7',
    'm1adr8': u'Адрес для примера 1.8',

    'm2adr1': u'Адрес для примера 2.1',
    'm2adr2': u'Адрес для примера 2.2',
    'm2adr3': u'Адрес для примера 2.3',
    'm2adr4': u'Адрес для примера 2.4',

    'm3adr1': u'Адрес для примера 3.1',
    'm3adr2': u'Адрес для примера 3.2',
    'm3adr3': u'Адрес для примера 3.3',
    'm4adr1': u'Адрес для примера 4.1',
    'm4adr2': u'Адрес для примера 4.2',
    'm4adr3': u'Адрес для примера 4.3',
    'm5adr1': u'Адрес для примера 5.1',
    'm5adr2': u'Адрес для примера 5.2',
    'm5adr3': u'Адрес для примера 5.3',


    'm1ctxt1': u'Контекст 1.1',
    'm1ctxt2': u'Контекст 1.2',
    'm1ctxt3': u'Контекст 1.3',
    'm1ctxt4': u'Контекст 1.4',
    'm1ctxt5': u'Контекст 1.5',
    'm1ctxt6': u'Контекст 1.6',
    'm1ctxt7': u'Контекст 1.7',
    'm1ctxt8': u'Контекст 1.8',

    'm2ctxt1': u'Контекст 2.1',
    'm2ctxt2': u'Контекст 2.2',
    'm2ctxt3': u'Контекст 2.3',
    'm2ctxt4': u'Контекст 2.4',

    'm3ctxt1': u'Контекст 3.1',
    'm3ctxt2': u'Контекст 3.2',
    'm3ctxt3': u'Контекст 3.3',
    'm4ctxt1': u'Контекст 4.1',
    'm4ctxt2': u'Контекст 4.2',
    'm4ctxt3': u'Контекст 4.3',
    'm5ctxt1': u'Контекст 5.1',
    'm5ctxt2': u'Контекст 5.2',
    'm5ctxt3': u'Контекст 5.3',


    'm1gr1': u'Греч. параллель для контекста 1.1',
    'm1gr2': u'Греч. параллель для контекста 1.2',
    'm1gr3': u'Греч. параллель для контекста 1.3',
    'm1gr4': u'Греч. параллель для контекста 1.4',
    'm1gr5': u'Греч. параллель для контекста 1.5',
    'm1gr6': u'Греч. параллель для контекста 1.6',
    'm1gr7': u'Греч. параллель для контекста 1.7',
    'm1gr8': u'Греч. параллель для контекста 1.8',

    'm2gr1': u'Греч. параллель для контекста 2.1',
    'm2gr2': u'Греч. параллель для контекста 2.2',
    'm2gr3': u'Греч. параллель для контекста 2.3',
    'm2gr4': u'Греч. параллель для контекста 2.4',

    'm3gr1': u'Греч. параллель для контекста 3.1',
    'm3gr2': u'Греч. параллель для контекста 3.2',
    'm3gr3': u'Греч. параллель для контекста 3.3',
    'm4gr1': u'Греч. параллель для контекста 4.1',
    'm4gr2': u'Греч. параллель для контекста 4.2',
    'm4gr3': u'Греч. параллель для контекста 4.3',
    'm5gr1': u'Греч. параллель для контекста 5.1',
    'm5gr2': u'Греч. параллель для контекста 5.2',
    'm5gr3': u'Греч. параллель для контекста 5.3',



    'mm1': u'Метафорическое употребление (1)',
    'mm2': u'Метафорическое употребление (2)',
    'mm3': u'Метафорическое употребление (3)',

    'mm1ex1': u'Пример для метафоры 1.1',
    'mm1ex2': u'Пример для метафоры 1.2',
    'mm1ex3': u'Пример для метафоры 1.3',
    'mm2ex1': u'Пример для метафоры 2.1',
    'mm2ex2': u'Пример для метафоры 2.2',
    'mm2ex3': u'Пример для метафоры 2.3',
    'mm3ex1': u'Пример для метафоры 3.1',
    'mm3ex2': u'Пример для метафоры 3.2',
    'mm3ex3': u'Пример для метафоры 3.3',

    'mm1adr1': u'Адрес для примера метафоры 1.1',
    'mm1adr2': u'Адрес для примера метафоры 1.2',
    'mm1adr3': u'Адрес для примера метафоры 1.3',
    'mm2adr1': u'Адрес для примера метафоры 2.1',
    'mm2adr2': u'Адрес для примера метафоры 2.2',
    'mm2adr3': u'Адрес для примера метафоры 2.3',
    'mm3adr1': u'Адрес для примера метафоры 3.1',
    'mm3adr2': u'Адрес для примера метафоры 3.2',
    'mm3adr3': u'Адрес для примера метафоры 3.3',


    'mm1ctxt1': u'Контекст для метафоры 1.1',
    'mm1ctxt2': u'Контекст для метафоры 1.2',
    'mm1ctxt3': u'Контекст для метафоры 1.3',
    'mm2ctxt1': u'Контекст для метафоры 2.1',
    'mm2ctxt2': u'Контекст для метафоры 2.2',
    'mm2ctxt3': u'Контекст для метафоры 2.3',
    'mm3ctxt1': u'Контекст для метафоры 3.1',
    'mm3ctxt2': u'Контекст для метафоры 3.2',
    'mm3ctxt3': u'Контекст для метафоры 3.3',

    'mm1gr1': u'Греч. параллель для метафоры 1.1',
    'mm1gr2': u'Греч. параллель для метафоры 1.2',
    'mm1gr3': u'Греч. параллель для метафоры 1.3',
    'mm2gr1': u'Греч. параллель для метафоры 2.1',
    'mm2gr2': u'Греч. параллель для метафоры 2.2',
    'mm2gr3': u'Греч. параллель для метафоры 2.3',
    'mm3gr1': u'Греч. параллель для метафоры 3.1',
    'mm3gr2': u'Греч. параллель для метафоры 3.2',
    'mm3gr3': u'Греч. параллель для метафоры 3.3',



    'cg1': u'Устойчивое сочетание (3)',
    'cg2': u'Устойчивое сочетание (1)',
    'cg3': u'Устойчивое сочетание (2)',
}


def g(column_name):
    return csv_columns[csv_translate[column_name]]

class MoodleEntry:
    def __init__(self):
        self.orthvars = []
        

@login_required
def import_moodle_base(request):

    if request.method == 'POST':
        form = BilletImportForm(request.POST, request.FILES)
        if form.is_valid():

            csvfile = request.FILES['csvfile']
            csv_reader = unicode_csv.UnicodeReader(csvfile, dialect=unicode_csv.calc, encoding='utf-8')

            output = StringIO.StringIO()
            csv_writer = unicode_csv.UnicodeWriter(output, dialect=unicode_csv.calc, encoding='utf-8')

            headers = csv_reader.next()
            csv_writer.writerow(headers)
            for n, column_name in enumerate(headers):
                if column_name not in csv_columns:
                    raise NameError(u'Не учтённое название столбца в CSV-файле.')
                csv_columns[column_name] = n

            idems = OrthographicVariant.objects.all().values_list('idem') # Список списков, каждый из которых содержит один элемент.
            idems = [x[0] for x in idems] # Переходим от списка списков к списку самих элементов (орфографических вариантов).
            authors = CustomUser.objects.all()

            orthvar_collisions = False
            csv_authors = {}

            for row in csv_reader:
                ENTRY = MoodleEntry()
                L = ('headword', 'orthvar1', 'orthvar2', 'orthvar3', 'orthvar4')
                ENTRY.orthvars = [row[g(i)].strip() for i in L if row[g(i)].strip()]

                for orthvar in ENTRY.orthvars:
                    if orthvar in idems:
                        orthvar_collisions = True
                        csv_writer.writerow(row)
                else:
                    author_in_csv = row[g('author')]
                    if author_in_csv in csv_authors:
                        author = csv_authors[author_in_csv]
                    else:
                        for au in authors:
                            if au.last_name and author_in_csv.startswith(au.last_name):
                                author = au
                                csv_authors[author_in_csv] = au
                                break
                        else:
                            raise NameError(u"Автор, указанный в CSV-файле, не найден среди участников работы над словарём.")

                    entry_args = entry_dict.copy() # Поверхностная (!) копия словаря.
                    entry_args['status'] = ccc
                    # Все булевские переменные уже выставлены по умолчанию в False в entry_dict

                    from_csv = {
                        'word_forms_list': word_forms_list,
                        'civil_equivalent': civil_equivalent,
                        'antconc_query': antconc_query,
                        'editor': author,
                        'additional_info': additional_info,
                    }
                    entry_args.update(from_csv)

                    entry = Entry.objects.create(**entry_args)
                    entry.save()

                    ov = OrthographicVariant.objects.create(entry=entry, idem=orthvar)
                    ov.save()

            if orthvar_collisions:
                response = HttpResponse(output.getvalue(), mimetype="text/csv")
                response['Content-Disposition'] = 'attachment; filename=%s--not.imported.csv' % datetime.datetime.strftime(datetime.datetime.now(), format='%Y.%m.%d--%H.%M.%S')
            else:
                response = HttpResponseRedirect('/')

            output.close()
            csvfile.close()
            return response
    else:
        form = BilletImportForm()
    return render_to_response('csv_import.html', {'form': form})
