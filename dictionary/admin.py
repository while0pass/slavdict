# -*- coding: UTF-8 -*-
from django.contrib import admin

from cslav_dict.dictionary.models import CivilEquivalent
admin.site.register(CivilEquivalent)

from cslav_dict.dictionary.models import OrthographicVariant
class OrthVar_Inline(admin.StackedInline):
    model = OrthographicVariant
    extra = 1
    fieldsets = (
        (None, {
            'fields': (
                (
                'idem',
                'is_headword',
                ),
                (
                'is_reconstructed',
                'is_approved',
                'frequency',
                ),
                #'is_factored_out'
                ),
            }),
        )

from cslav_dict.dictionary.models import Etymology 
admin.site.register(Etymology)
    
from cslav_dict.dictionary.models import ProperNoun
class ProperNoun_Inline(admin.StackedInline):
    model = ProperNoun
    max_num = 1
#    fieldsets = (
#        (None, {
#            'fields':  ('onym',),
#            'classes': ('collapse',),
#            }),
#        )

from cslav_dict.dictionary.models import Address
admin.site.register(Address)

from cslav_dict.dictionary.models import Example
class Example_Inline(admin.StackedInline):
    model = Example
    extra = 1

from cslav_dict.dictionary.models import Meaning
admin.site.register(
    Meaning,
    inlines = (
        Example_Inline,
        )
    )

def entry_with_orth_variants(obj):
    orth_vars = [unicode(i) for i in obj.orthographic_variants.all().order_by('-is_headword','idem')]
    delimiter = u', '
    x = delimiter.join(orth_vars)
    return u'%s (%s)' % (obj.civil_equivalent.text, x)

entry_with_orth_variants.admin_order_field = 'civil_equivalent'
entry_with_orth_variants.short_description = u'словарная статья'


from cslav_dict.dictionary.models import Entry
admin.site.register(
    Entry,
    fieldsets = (
        (None, {
            'fields': (
                'civil_equivalent',
                'part_of_speech',
                'uninflected',
                ),
            }),
        (u'для существительных', {
            'fields': (
                'genitive',
                'gender',
                'tantum',
                ),
            'classes': (
                'collapse',
                ),
            }),
        (u'для прилагательных', {
            'fields': (
                'short_form',
                ),
            'classes': (
                'collapse',
                ),
            }),
        (u'для глаголов', {
            'fields': (
                'transitivity',
                'sg1',
                'sg2',
                ),
            'classes': (
                'collapse',
                ),
            }),
        ),
    inlines = (
        OrthVar_Inline,
        ProperNoun_Inline,
        ),
    list_display = (
        entry_with_orth_variants,
        'part_of_speech',
        ),
    list_filter = (
        'part_of_speech',
        #'editor',
        #'status',
        ),
)
