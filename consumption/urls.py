from django.conf.urls import patterns, include, url

from django.contrib import admin
from consumption.views import GraphicView, importCSV, exportCSV, ajaxPlot
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
  url(r'^$', GraphicView.as_view(), name='graphic'),
  url(r'^importCSV$', importCSV, name='importCSV'),
  url(r'^exportCSV$', exportCSV, name='exportCSV'),
  url(r'^ajaxPlot$', ajaxPlot, name='ajaxPlot'),

)
