from django.conf.urls import patterns, include, url

from django.contrib import admin
from consumption.views import GraphicView, importCSV, exportCSV, ajaxPlot
admin.autodiscover()

from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    # Examples:
  url(r'^$', login_required(GraphicView.as_view()), name='graphic'),
  url(r'^importCSV$', login_required(importCSV), name='importCSV'),
  url(r'^exportCSV$', login_required(exportCSV), name='exportCSV'),
  url(r'^ajaxPlot$', login_required(ajaxPlot), name='ajaxPlot'),

)
