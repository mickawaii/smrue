from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from configuration.views import ConfigView

urlpatterns = patterns('',
    url(r'^$', ConfigView.as_view(), name='config'),
)