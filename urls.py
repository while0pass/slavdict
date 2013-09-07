# -*- coding: utf-8 -*-

from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import RedirectView

from slavdict.admin import ui
admin.autodiscover()

urlpatterns = patterns('',
    url( r'^admin/',     include(admin.site.urls) ),
    url( r'^admin/doc/', include('django.contrib.admindocs.urls') ),
    url( r'^ui/',        include(ui.urls) ),
)

urlpatterns += patterns('',
    url( r'^$', 'slavdict.dictionary.views.entry_list', name='all_entries_url' ),
    url( r'^login/$', 'django.contrib.auth.views.login'),
    url( r'^logout/$', 'django.contrib.auth.views.logout_then_login'),

    url( r'^print/$', RedirectView.as_view(url='/print/entries/')),
    url( r'^print/entries/$', 'slavdict.dictionary.views.all_entries' ),
    url( r'^print/examples/$', 'slavdict.dictionary.views.all_examples' ),
    url( r'^print/examples/audit/$', 'slavdict.dictionary.views.all_examples',
                                      kwargs={'mark_as_audited': True} ),
    url( r'^print/examples/unaudit/$', 'slavdict.dictionary.views.all_examples',
                                        kwargs={'mark_as_unaudited': True} ),
    url( r'^cherry-pick/$', 'slavdict.dictionary.views.all_entries', kwargs={'is_paged': True} ),

    url( r'^entries/(\d+)/$', 'slavdict.dictionary.views.single_entry', name='single_entry_url' ),
    url( r'^entries/(\d+)/intermed/$',
         'slavdict.dictionary.views.single_entry',
         kwargs={'extra_context': {'show_additional_info': True, 'intermed': True}},
         name="intermediary_change_form_url"),
    url( r'^entries/(\d+)/edit/$', 'slavdict.dictionary.views.edit_entry',
         name='edit_form_url'),
    url( r'^entries/(\d+)/get/$', 'slavdict.dictionary.jsonviews.json_entry_get' ),
    url( r'^entries/save/$', 'slavdict.dictionary.jsonviews.json_entry_save' ),
    url( r'^entries/jserror/$', 'slavdict.dictionary.jsonviews.js_error_notify' ),

    url(r'^materials/$', 'slavdict.dictionary.views.direct_to_template',
                         kwargs={'template': 'materials.html'}),
    url( r'^switch/additional-info/$', 'slavdict.dictionary.views.switch_additional_info', name='switch_info_url' ),
    url( r'^converter/$', 'slavdict.dictionary.views.antconc2ucs8_converter', name='converter' ),

    url( r'^json/singleselect/entries/urls/$', 'dictionary.jsonviews.json_singleselect_entries_urls'),

    url( r'^greek/$', 'dictionary.views.hellinist_workbench', name='hellinist_workbench' ),
    url( r'^json/greq/save/$', 'dictionary.jsonviews.json_greq_save', name="jsonGreqSaveURL"),
    url( r'^json/greq/delete/$', 'dictionary.jsonviews.json_greq_delete', name="jsonGreqDeleteURL"),
    url( r'^json/ex/save/$', 'dictionary.jsonviews.json_ex_save', name="jsonExSaveURL"),
    url( r'^json/goodness/save/$', 'dictionary.jsonviews.json_goodness_save', name="jsonGoodnessSaveURL"),

    # TODO: В последствии всё это должно быть удалено.
    url( r'^adhoc/csv-import/$', 'slavdict.dictionary.views.import_csv_billet' ),
    url( r'^adhoc/dump/$', 'slavdict.dictionary.views.dump' ),
)

urlpatterns += staticfiles_urlpatterns()
