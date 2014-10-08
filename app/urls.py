from django.conf.urls import patterns, url

urlpatterns = patterns('snippets.views',
    url(r'^api/v1/people/(?P<pk>[0-9]+)/$', 'people_detail'),

)
