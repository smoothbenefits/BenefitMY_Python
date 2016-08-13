from StringIO import StringIO

from django.db import transaction
from django.http import Http404
from django.contrib.auth import get_user_model
from django import template
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import get_template
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from app.models.extra_benefits.person_company_extra_benefit_plan import \
    PersonCompanyExtraBenefitPlan
from app.models.extra_benefits.person_company_extra_benefit_plan_item import \
    PersonCompanyExtraBenefitPlanItem
from app.serializers.extra_benefits.person_company_extra_benefit_plan_serializer import (
    PersonCompanyExtraBenefitPlanSerializer,
    PersonCompanyExtraBenefitPlanPostSerializer)
from app.service.send_email_service import SendEmailService
from app.view_models.person_info import PersonInfo


class PersonCompanyExtraBenefitPlanView(APIView):
    """ single employee benefit """
    def _get_object(self, pk):
        try:
            return PersonCompanyExtraBenefitPlan.objects.get(pk=pk)
        except PersonCompanyExtraBenefitPlan.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        plan = self._get_object(pk)
        serializer = PersonCompanyExtraBenefitPlanSerializer(plan)
        return Response(serializer.data)

    @transaction.atomic
    def delete(self, request, pk, format=None):
        plan = self._get_object(pk)
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    def put(self, request, pk, format=None):
        plan = self._get_object(pk)
        serializer = PersonCompanyExtraBenefitPlanPostSerializer(plan, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            self._send_email(serializer.object)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def post(self, request, pk, format=None):
        serializer = PersonCompanyExtraBenefitPlanPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            self._send_email(serializer.object)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _send_email(self, person_company_extra_benefit_plan_model):
        # Construct a "view model" to pipe in the context information
        has_interests = False
        plan_items = []
        for item in person_company_extra_benefit_plan_model.plan_items.all():
            has_interests = has_interests or item.opt_in
            plan_items.append({
                'item_name': item.extra_benefit_item.name,
                'opt_in': 'Yes' if item.opt_in else 'No'
            })

        context_data = {
            'company': person_company_extra_benefit_plan_model.company_plan.company,
            'person': PersonInfo(person_company_extra_benefit_plan_model.person),
            'plan_items': plan_items
        }

        # Skip sending the email if employee did not show interest
        # on any of the items
        if (not has_interests):
            return

        send_email_service = SendEmailService()

        subject = 'Individual Benefits Interests Notification'
        html_template_path = 'email/extra_benefit_interest_notification.html'
        txt_template_path = 'email/extra_benefit_interest_notification.txt'

        # build the list of target emails
        company_id = person_company_extra_benefit_plan_model.company_plan.company.id
        broker_emails = send_email_service.get_broker_emails_by_company(company_id)

        # build the template context data
        context_data = {'context_data':context_data, 'site_url':settings.SITE_URL}

        send_email_service.send_support_email(
            broker_emails, subject, context_data, html_template_path, txt_template_path)

        return

class PersonCompanyExtraBenefitPlanByPersonView(APIView):
    """ Commuter plan enrollment for a single employee """
    def _get_object(self, person_id):
        try:
            return PersonCompanyExtraBenefitPlan.objects.filter(person=person_id)
        except PersonCompanyExtraBenefitPlan.DoesNotExist:
            raise Http404

    def get(self, request, person_id, format=None):
        plans = self._get_object(person_id)
        serializer = PersonCompanyExtraBenefitPlanSerializer(plans, many=True)
        return Response(serializer.data)
