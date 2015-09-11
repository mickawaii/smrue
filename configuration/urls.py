from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from configuration.views import ConfigView, UserCreateView, UserUpdateView, PasswordUpdateView, PasswordRecoverView, PasswordRecoverDoneView, PasswordResetView, PasswordResetDoneView

from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^$', login_required(ConfigView.as_view()), name='config'),
    url(r'^user$', UserCreateView.as_view(), name='create_user'),
    url(r'^user/edit$', login_required(UserUpdateView.as_view()), name='edit_user'),
    url(r'^user/change_password$', login_required(PasswordUpdateView.as_view()), name='edit_password'),
    url(r'^user/recover_password$', PasswordRecoverView().recover_password, name='recover_password'),
    url(r'^user/recover_password_done$', PasswordRecoverDoneView.as_view(), name='recover_password_done'),
    url(r'^user/reset_password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', PasswordResetView().reset_password, name='reset_password'),
    url(r'^user/reset_password_done$', PasswordResetDoneView.as_view(), name='reset_password_done'),
)