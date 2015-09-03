from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from goal.views import IndexView, CreateView, DeleteView, UpdateView

from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^$', login_required(IndexView.as_view()), name='list'),
    url(r'^create$', login_required(CreateView.as_view()), name='create'),
    url(r'^delete/(?P<pk>\d+)$', login_required(DeleteView.as_view()), name='delete'), 
    url(r'^(?P<pk>\d+)$', login_required(UpdateView.as_view()), name='update'), 
)
