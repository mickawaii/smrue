from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from sensor.views import IndexView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='list')
)