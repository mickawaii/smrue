from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from configuration.views import ConfigView, UserView

urlpatterns = patterns('',
    url(r'^$', ConfigView.as_view(), name='config'),
    url(r'user/(?P<user_pk>\d+)$', UserView.as_view(), name='user'),
)