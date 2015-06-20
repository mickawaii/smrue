from django.conf.urls import patterns, include, url

from django.contrib import admin
from consumption.views import GraphicView
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', GraphicView.as_view(), name='graphic'),
)
