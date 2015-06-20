from django.conf.urls import patterns, include, url

from django.contrib import admin
from consumption.views import graphicView
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
  url(r'^$', graphicView, name='graphic'),
)
