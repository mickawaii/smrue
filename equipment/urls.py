from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from equipment.views import IndexView, CreateView, DeleteView, UpdateView

from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^$', login_required(IndexView.as_view()), name='list'),
    url(r'^create$', login_required(CreateView.as_view()), name='create'),
    url(r'^(?P<pk>\d+)/delete$', login_required(DeleteView.as_view()), name='delete'),
    url(r'^(?P<pk>\d+)/edit$', login_required(UpdateView.as_view()), name='edit'),
)