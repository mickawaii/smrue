from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from sensor.views import IndexView, DeleteView

from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^$', login_required(IndexView.as_view()), name='list'),
    url(r'^(?P<pk>\d+)/delete$', login_required(DeleteView.as_view()), name='delete'),   
)