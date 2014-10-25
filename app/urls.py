from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns


from app.views.person_view import PersonView
from app.views.user_view import UserView, UsersView, UserFamilyView
from app.views.company_user_view import CompanyUserView
from app.views.benefit_type_view import BenefitTypeView
from app.views.document_type_view import DocumentTypeView
from app.views.company_view import CompanyView
from app.views import dashboard_view

from app.views.template_view import TemplateView

from app.views.company_benefit_plan_option_view import (
    CompanyBenefitPlanOptionView,
    CompanyBenefitPlansView
    )

from app.views.document_view import DocumentView
from app.views.company_templates_view import CompanyTemplatesView

PREFIX = "api/v1"

urlpatterns = patterns('app.views',
    url(r'^dashboard/$', dashboard_view.index, name='dashboard'),
    url(r'^%s/people/(?P<pk>[0-9]+)/$' % PREFIX, PersonView.as_view()),

    url(r'^%s/benefit_types/$' % PREFIX, BenefitTypeView.as_view()),

    url(r'^%s/document_types/$' % PREFIX, DocumentTypeView.as_view()),

    url(r'^%s/companies/(?P<pk>[0-9]+)/$' % PREFIX, CompanyView.as_view()),

    url(r'^%s/users/$' % PREFIX, UsersView.as_view()),
    url(r'^%s/users/(?P<pk>[0-9]+)/$' % PREFIX, UserView.as_view()),
    url(r'^%s/users/(?P<pk>[0-9]+)/family/$' % PREFIX, UserFamilyView.as_view()),
    url(r'^%s/templates/(?P<pk>[0-9]+)/$' % PREFIX, TemplateView.as_view()),
    url(r'^%s/benefits/(?P<pk>[0-9]+)/$' % PREFIX, CompanyBenefitPlanOptionView.as_view()),

    url(r'^%s/companies/(?P<pk>[0-9]+)/benefits/$' % PREFIX,
        CompanyBenefitPlansView.as_view()),

    url(r'^%s/companies/(?P<pk>[0-9]+)/users/$' % PREFIX, CompanyUserView.as_view()),
    url(r'^%s/companies/(?P<pk>[0-9]+)/documents/$' % PREFIX, DocumentView.as_view()),
    url(r'^%s/companies/(?P<pk>[0-9]+)/templates/$' % PREFIX, CompanyTemplatesView.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)
