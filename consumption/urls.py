from django.conf.urls import patterns, include, url

from django.contrib import admin
from consumption.views import GraphicView, importCSV, exportCSV, ajaxPlot, create
admin.autodiscover()

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

urlpatterns = patterns('',
    # Examples:
  url(r'^$', login_required(GraphicView.as_view()), name='graphic'),
  url(r'^importCSV$', login_required(importCSV), name='importCSV'),
  url(r'^exportCSV$', login_required(exportCSV), name='exportCSV'),
  url(r'^ajaxPlot$', login_required(ajaxPlot), name='ajaxPlot'),
  url(r'^create$', csrf_exempt(create), name='create'),

)
