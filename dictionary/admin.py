# encoding: UTF-8
from django.conf import settings
from django import forms
from django.db import models
from django.contrib import admin

def _orth_vars(obj):
    orth_vars = [unicode(i) for i in obj.orthographic_variants.all().order_by('id')]
    delimiter = u', '
    return delimiter.join(orth_vars)

def _collocations(obj):
    collocations = [unicode(i) for i in obj.collocation_set.all().order_by('id')]
    delimiter = u', '
    return delimiter.join(collocations)

def entry_with_orth_variants(obj):
    if obj.homonym_order:
        h = u' %s' % unicode(obj.homonym_order)
    else:
        h = u''
    x = _orth_vars(obj)
    e = obj.civil_equivalent
    if e:
        result = u'%s%s (%s%s)' % (x, h, e, h)
    else:
        result = u'%s%s' % (x, h)
    return result

entry_with_orth_variants.admin_order_field = 'civil_equivalent'
entry_with_orth_variants.short_description = u'словарная статья'

def meaning_with_entry(obj):
    econtainer = obj.entry_container
    if econtainer:
        ent = entry_with_orth_variants(econtainer)
    else:
        cgcontainer = obj.collogroup_container
        if cgcontainer:
            ent = _collocations(cgcontainer)
        else:
            ent = u'(БЕСХОЗНОЕ ЗНАЧЕНИЕ)'
    return u'%s [%s] %s' % (ent, obj.id, obj.meaning)

meaning_with_entry.admin_order_field = 'entry_container'
meaning_with_entry.short_description = u'значение'

def example_with_entry(obj):
    return u'%s [%s] %s' % (meaning_with_entry(obj.meaning), obj.id, obj.example)


from slavdict.dictionary.models import OrthographicVariant
class OrthVar_Inline(admin.StackedInline):
    model = OrthographicVariant
    extra = 1
    fieldsets = (
        (None, {
            'fields': (('idem', 'is_reconstructed'),),
            }),
        )

from slavdict.dictionary.models import Etymology
ETYMOLOGY_FIELDSETS = (
    (u'Является этимоном для др. этимона',
        {'fields': (('etymon_to', 'questionable'),),
        'classes': ('collapse',)}
        ),
    (None,
        {'fields': ('language', ('text', 'translit'), ('meaning', 'gloss'), ('unclear', 'mark'))}
        ),
    (u'Доп. инфо.',
        {'fields': ('additional_info',),
        'classes': ('collapse',)}
        ),
    )
class Etymology_Inline(admin.StackedInline):
    model = Etymology
    extra = 0
    fieldsets = ETYMOLOGY_FIELDSETS

class EtymologyForCollocation_Inline(admin.StackedInline):
    model = Etymology
    extra = 1
    fieldsets = ETYMOLOGY_FIELDSETS

from slavdict.dictionary.models import GreekEquivalentForMeaning
class GreekEquivalentForMeaning_Inline(admin.StackedInline):
    model = GreekEquivalentForMeaning
    extra = 0
    fieldsets = (
        (None, {
            'fields': (('text', 'mark'),),
            }),
        )

from slavdict.dictionary.models import GreekEquivalentForExample
class GreekEquivalentForExample_Inline(admin.StackedInline):
    model = GreekEquivalentForExample
    extra = 0
    fieldsets = (
        (None, {
            'fields': (('text', 'mark', 'position'),),
            }),
        )

from slavdict.dictionary.models import ProperNoun
class ProperNoun_Inline(admin.StackedInline):
    model = ProperNoun
    extra = 0
    max_num = 1




from slavdict.dictionary.models import Example
Example.__unicode__=lambda self:example_with_entry(self)

EXAMPLE_FIELDSETS = (
        (None, {'fields': (('example', 'address_text'),)}),
        (u'Доп. инфо.', {'fields': ('additional_info',), 'classes': ('collapse',)}),
    )

class Example_Inline(admin.StackedInline):
    model = Example
    extra = 1
    fieldsets = EXAMPLE_FIELDSETS
    formfield_overrides = { models.TextField: {'widget': forms.Textarea(attrs={'rows':'2'})}, }

class AdminExample(admin.ModelAdmin):
    inlines = (GreekEquivalentForExample_Inline,)
    fieldsets = ((None, {'fields': ('meaning',)}),) + EXAMPLE_FIELDSETS
    formfield_overrides = { models.TextField: {'widget': forms.Textarea(attrs={'rows':'2'})}, }
    ordering = ('-id',)
    list_display = ('id', '__unicode__')
    list_display_links = list_display
    class Media:
        css = {"all": (settings.MEDIA_URL + "fix_admin.css",)}

admin.site.register(Example, AdminExample)




from slavdict.dictionary.models import MeaningContext
class MeaningContext_Inline(admin.StackedInline):
    model = MeaningContext
    extra = 0
    fieldsets = ((None, {'fields': ('context', ('left_text', 'right_text'),)}),)

from slavdict.dictionary.models import Meaning
Meaning.__unicode__=lambda self:meaning_with_entry(self)
class AdminMeaning(admin.ModelAdmin):
    inlines = (
        Example_Inline,
        GreekEquivalentForMeaning_Inline,
        MeaningContext_Inline,
        )
    fieldsets = (
            (u'То, к чему значение относится',
                {'fields': (('entry_container', 'collogroup_container'),)}),
            (u'Если является подзначением',
                {'fields': ('parent_meaning',),
                'classes': ('collapse',)}),
            (u'См.',
                {'fields': (('link_to_entry', 'link_to_collogroup'), 'link_to_meaning'),
                'classes': ('collapse',)}),
            (u'Ср.',
                {'fields': (('cf_entries', 'cf_collogroups'), 'cf_meanings'),
                'classes': ('collapse',)}),
            (u'В роли сущ.',
                {'fields': (('substantivus', 'substantivus_type'),),
                'classes': ('collapse',)}),
            (None,
                {'fields': ('metaphorical', ('meaning', 'gloss'))}),
            (u'Доп. инфо.',
                {'fields': ('additional_info',),
                'classes': ('collapse',)}),
        )
    save_on_top = True
    formfield_overrides = { models.TextField: {'widget': forms.Textarea(attrs={'rows':'2'})}, }
    filter_horizontal = ('cf_entries', 'cf_collogroups', 'cf_meanings')
    ordering = ('-id',)
    list_display = ('id', '__unicode__')
    list_display_links = list_display

    class Media:
        css = {"all": (settings.MEDIA_URL + "fix_admin.css",)}

admin.site.register(Meaning, AdminMeaning)


from slavdict.dictionary.models import Entry
Entry.__unicode__=lambda self: entry_with_orth_variants(self)
class AdminEntry(admin.ModelAdmin):
    fieldsets = (
        (u'Омонимия', {
            'fields': (('homonym_order', 'homonym_gloss'),),
            'classes': ('collapse',) } ),
        (None, {
            'fields': (('civil_equivalent', 'part_of_speech', 'editor'),),
            }),
        (u'Для сущ.', {
            'fields': (('genitive', 'gender', 'tantum'),),
            'classes': ('collapse',) } ),
        (u'Для прил.', {
            'fields': (('short_form', 'possessive'),),
            'classes': ('collapse',) } ),
        (None, {
            'fields': ('uninflected',),}),
        (u'Для глаг.', { 'fields': (('sg1', 'sg2'),), 'classes': ('collapse',) } ),
        (u'Образовано от', { 'fields': ( 'derivation_entry',), 'classes': ( 'collapse',), }),
        (u'См.',
            {'fields': (('link_to_entry', 'link_to_collogroup'), 'link_to_meaning'),
            'classes': ('collapse',)}),
        (u'Ср.',
            {'fields': (('cf_entries', 'cf_collogroups'), 'cf_meanings'),
            'classes': ('collapse',)}),
        (u'Доп. инфо.', {
            'fields':  ('additional_info',),
            'classes': ('collapse',) }),
        (u'Адм. инфо.', {
            'fields': (('status', 'percent_status', 'grequiv_status'),),
            'classes': ('collapse',) }),
        )
    inlines = (
        OrthVar_Inline,
        Etymology_Inline,
        ProperNoun_Inline,
        )
    list_display = (
        'id',
        'civil_equivalent',
        '__unicode__',
        'part_of_speech',
        'editor',
        )
    list_display_links = (
        'id',
        'civil_equivalent',
        '__unicode__',
        )
    list_filter = (
        'editor',
        )
    filter_horizontal = ('cf_entries', 'cf_collogroups', 'cf_meanings')
    ordering = ('-id',)
    save_on_top = True
    formfield_overrides = { models.TextField: {'widget': forms.Textarea(attrs={'rows':'2'})}, }

    class Media:
        css = {"all": (settings.MEDIA_URL + "fix_admin.css",)}

admin.site.register(Entry, AdminEntry)

from slavdict.dictionary.models import SynonymGroup
admin.site.register(SynonymGroup)


from slavdict.dictionary.models import Collocation
class AdminCollocation(admin.ModelAdmin):
    inlines = (EtymologyForCollocation_Inline,)
    fieldsets = (
            (None, {'fields': (('collocation', 'civil_equivalent'),)}),
        )
    class Media:
        css = {"all": (settings.MEDIA_URL + "fix_admin.css",)}

admin.site.register(Collocation, AdminCollocation)

class Collocation_Inline(admin.StackedInline):
    model = Collocation
    extra = 1
    fieldsets = (
            (None, {'fields': ('collocation',)}),
        )

from slavdict.dictionary.models import CollocationGroup
CollocationGroup.__unicode__=lambda self: _collocations(self)
class AdminCollocationGroup(admin.ModelAdmin):
    inlines = (Collocation_Inline,)
    fieldsets = (
            (None,
                {'fields': (('base_meaning', 'base_entry'),)}),
            (u'См.',
                {'fields': ('link_to_entry', 'link_to_meaning'),
                'classes': ('collapse',)}),
            (u'Ср.',
                {'fields': ('cf_entries', 'cf_meanings'),
                'classes': ('collapse',)}),
        )
    ordering = ('-id',)
    filter_horizontal = ('cf_entries', 'cf_meanings')
    list_display = ('id', '__unicode__')
    list_display_links = list_display
    class Media:
        css = {"all": (settings.MEDIA_URL + "fix_admin.css",)}

admin.site.register(CollocationGroup, AdminCollocationGroup)
