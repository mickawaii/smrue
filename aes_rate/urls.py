
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # url(r'^$', views.IndexView.as_view(), name='home'),
    url(r'^$', IndexView.as_view(), name='list')

    # url(r'^list$', pivot_tables.IndexView().pivot_table_presets_delete, name='pivot_table_presets_delete'),
    # url(r'^cr/preset/(?P<preset_pk>\d+)/delete$', pivot_tables.IndexView().pivot_table_presets_delete, name='pivot_table_presets_delete'),
)