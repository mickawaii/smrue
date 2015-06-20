from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from equipment.views import IndexView, CreateView, DeleteView, UpdateView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='list'),
    url(r'^create$', CreateView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/delete$', DeleteView.as_view(), name='delete'),
    url(r'^(?P<pk>\d+)/edit$', UpdateView.as_view(), name='edit'),
)