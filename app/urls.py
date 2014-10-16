from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns


from app.views.person_view import PersonView
from app.views.user_view import User_Detail, Users, UserFamilyView
from app.views.company_user_view import CompanyUserView


urlpatterns = patterns('app.views',
    url(r'^api/v1/people/(?P<pk>[0-9]+)/$', PersonView.as_view()),

    url(r'^api/v1/users/(?P<pk>[0-9]+)/$', User_Detail.as_view()),
    url(r'^api/v1/users/$', Users.as_view()),


    url(r'^api/v1/companies/(?P<pk>[0-9]+)/users/$', CompanyUserView.as_view()),

    url(r'^api/v1/users/(?P<pk>[0-9]+)/family/$', UserFamilyView.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)
