from django.conf.urls import patterns, include, url
from smrue import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.HomeView.as_view(), name='home'),
    # url(r'^consumption/', include('consumption.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # url(r'^goals/', include('goal.urls', namespace="goal"))
    url(r'^equipments/', include('equipment.urls', namespace="equipment")),
    url(r'^sensors/', include('sensor.urls', namespace="sensor")),
    url(r'^goals/', include('goal.urls', namespace="goal")),
    url(r'^consumption/', include('consumption.urls', namespace="consumption")),
    
)