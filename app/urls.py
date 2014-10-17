from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns


from app.views.person_view import PersonView
from app.views.user_view import UserView, UsersView, UserFamilyView
from app.views.company_user_view import CompanyUserView
from app.view.company_benefit_plan_option_view import (
    CompanyBenefitPlanOptionView,
    CompanyBenefitPlansView)

PREFIX = "api/v1"

urlpatterns = patterns('app.views',
    url(r'^%s/people/(?P<pk>[0-9]+)/$' % PREFIX, PersonView.as_view()),

    url(r'^%s/users/(?P<pk>[0-9]+)/$' % PREFIX, UserView.as_view()),
    url(r'^%s/users/$' % PREFIX, UsersView.as_view()),


    url(r'^%s/companies/(?P<pk>[0-9]+)/users/$' % PREFIX, CompanyUserView.as_view()),

    url(r'^%s/users/(?P<pk>[0-9]+)/family/$' % PREFIX, UserFamilyView.as_view()),

    url(r'^%s/benefits/(?P<pk>[0-9]+)/$' % PREFIX, CompanyBenefitPlanOptionView.as_view()),
    url(r'^%s/companies/(?P<pk>[0-9]+)/benefits/$' % PREFIX,
        CompanyBenefitPlansView.as_view()),

    url(r'^%s/companies/(?P<pk>[0-9]+)/documents/$' % PREFIX, DocumentView.as_view()),

    url(r'^%s/company/(?P<pk>[0-9]+)/$' % PREFIX, CompanyView.as_view()),

    url(r'^%s/document_types/$' % PREFIX, DocumentType.as_view()),

                       )

urlpatterns = format_suffix_patterns(urlpatterns)
