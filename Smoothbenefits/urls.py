from django.conf.urls import patterns, include, url
from django.contrib import admin
from app.views import register_view, login_view, home_view
from django.conf import settings


urlpatterns = patterns('',
    # Examples:
    url(r'^$', home_view.index, name='home'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^employee/signup/(?P<user_id>\w+)/?$', register_view.register_employee),
    url(r'^signup/$', register_view.register),
    url(r'^login/(?P<info_message>\w+)/?$', login_view.user_login, name='user_login_with_message'),
    url(r'^login/$', login_view.user_login, name='user_login'),
    url(r'^logout/$', login_view.user_logout, name='user_logout'),
    url(r'^', include('app.urls')),
)
urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
