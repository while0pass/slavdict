# -*- coding: utf-8 -*-
import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse

from dictionary.models import Entry
from dictionary.models import Example
from dictionary.models import GreekEquivalentForExample

def _json(x):
    return json.dumps(x, ensure_ascii=False, separators=(',',':'))

@login_required
def json_multiselect_entries(request):
    httpGET_FIND = request.GET.get('find')
    httpGET_ID = request.GET.get('ids')
    if httpGET_ID:
        httpGET_IDS = [httpGET_ID]
    else:
        httpGET_IDS = request.GET.getlist('ids[]')
        httpGET_IDS = [id for id in httpGET_IDS if id]
    if httpGET_FIND:
        FIND_LOWER = httpGET_FIND.lower()
        FIND_CAPZD = httpGET_FIND.capitalize()
        entries = Entry.objects \
            .filter(
                Q(civil_equivalent__startswith=FIND_LOWER)
                |
                Q(civil_equivalent__startswith=FIND_CAPZD)
            ).exclude(pk__in=httpGET_IDS) \
            .order_by('civil_equivalent', 'homonym_order')[:7]
        entries = [
            {
            'civil': e.civil_equivalent,
            'headword': e.orth_vars[0].idem_ucs,
            'pk': e.id,
            'hom': e.homonym_order_roman,
            'pos': e.part_of_speech.tag if e.homonym_order else '',
            'hint': e.homonym_gloss,
            'index': n,
            }
            for n, e in enumerate(entries)]
        data = _json(entries)
        response = HttpResponse(data, mimetype='application/json')
    else:
        response = HttpResponse(mimetype='application/json', status=400)
    return response

@login_required
def json_singleselect_entries_urls(request):
    httpGET_FIND = request.GET.get('find')
    if httpGET_FIND:
        FIND_LOWER = httpGET_FIND.lower()
        FIND_CAPZD = httpGET_FIND.capitalize()
        entries = Entry.objects \
            .filter(
                Q(civil_equivalent__startswith=FIND_LOWER)
                |
                Q(civil_equivalent__startswith=FIND_CAPZD)
            ).order_by('civil_equivalent', 'homonym_order')[:7]
        entries = [
                {
                'civil': e.civil_equivalent,
                'headword': e.orth_vars[0].idem_ucs,
                'hom': e.homonym_order_roman,
                'pos': e.part_of_speech.tag if e.homonym_order \
                    and e.part_of_speech \
                    and e.part_of_speech.slug not in ('letter', 'number')
                    else '',
                'hint': e.homonym_gloss,
                'url': e.get_absolute_url(),
                }
                for e in entries]
        data = _json(entries)
        response = HttpResponse(data, mimetype='application/json')
    else:
        response = HttpResponse(mimetype='application/json', status=400)
    return response



@login_required
def json_ex_save(request):
    jsonEx = request.POST.get('ex')
    if jsonEx:
        exDict = json.loads(jsonEx)
        ex = Example.objects.get(pk=int(exDict['id']))
        del exDict['id']
        ex.__dict__.update(exDict)
        ex.save()
        data = _json({ 'action': 'saved' })
        response = HttpResponse(data, mimetype='application/json', status=200)
    else:
        response = HttpResponse(status=400)
    return response


@login_required
def json_greq_save(request):
    jsonGreq = request.POST.get('greq')
    if jsonGreq:
        greq = json.loads(jsonGreq)
        if not greq['id']:
            del greq['id']
            gr = GreekEquivalentForExample(**greq)
            gr.save()
            data = _json({ 'action': 'created', 'id': gr.id })
        else:
            gr = GreekEquivalentForExample.objects.get(pk=int(greq['id']))
            gr.__dict__.update(greq)
            gr.save()
            data = _json({ 'action': 'saved' })
        response = HttpResponse(data, mimetype='application/json', status=200)
    else:
        response = HttpResponse(status=400)
    return response


@login_required
def json_greq_delete(request):
    jsonDelete = request.POST.get('delete')
    if jsonDelete:
        id = int( json.loads(jsonDelete) )
        if id:
            gr = GreekEquivalentForExample.objects.get(pk=id)
            gr.delete()
            data = _json({ 'action': 'deleted' })
            response = HttpResponse(data, mimetype='application/json', status=200)
        else:
            response = HttpResponse(status=400)
    else:
        response = HttpResponse(status=400)
    return response