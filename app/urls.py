from django.conf.urls import patterns, url
from app.views.person_view import PersonView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('snippets.views',
    url(r'^api/v1/people/(?P<pk>[0-9]+)/$', PersonView.as_view()),
)
urlpatterns = format_suffix_patterns(urlpatterns)
