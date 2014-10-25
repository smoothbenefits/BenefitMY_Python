from django.conf.urls import patterns, include, url
from django.contrib import admin
from app.views import register_view, login_view, home_view


urlpatterns = patterns('',
    # Examples:
    url(r'^$', home_view.index, name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^register/$', register_view.register),
    
    url(r'^login/$', login_view.user_login, name='user_login'),
    url(r'^', include('app.urls')),
)
