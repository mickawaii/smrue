
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from aes_rate.views import IndexView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='table'),
    url(r'^refresh_rates$', IndexView().refresh_rates, name='refresh_rates')
)