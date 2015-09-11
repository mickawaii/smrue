
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from aes_rate.views import IndexView

from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^$', login_required(IndexView.as_view()), name='table'),
    url(r'^refresh_rates$', login_required(IndexView().refresh_rates), name='refresh_rates')
)