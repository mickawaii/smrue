from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from goal.views import IndexView, CreateView, DeleteView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='list'),
    url(r'^create$', CreateView.as_view(), name='create'),
       
)
