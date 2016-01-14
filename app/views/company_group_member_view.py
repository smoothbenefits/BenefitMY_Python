from rest_framework.views import APIView
from django.http import Http404
from StringIO import StringIO
from rest_framework.response import Response
from rest_framework import status
from app.models.company_group import CompanyGroup
from app.models.company_group_member import CompanyGroupMember 
from app.models.person import (Person, SELF)
from app.serializers.company_group_member_serializer import (
    CompanyGroupMemberSerializer,
    CompanyGroupMemberPostSerializer,
    CompanyGroupWithMemberSerializer)
from app.service.send_email_service import SendEmailService
from app.service.Report.company_employee_benefit_pdf_report_service import \
    CompanyEmployeeBenefitPdfReportService


class CompanyGroupMemberView(APIView):
    def _get_object(self, pk):
        try:
            return CompanyGroupMember.objects.get(pk=pk)
        except CompanyGroupMember.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        group_member = self._get_object(pk)
        serializer = CompanyGroupMemberSerializer(group_member)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        company_group_member = self._get_object(pk)

        group_member_change_info = {
            'user': company_group_member.user,
            'company': company_group_member.company_group.company,
            'original_company_group': company_group_member.company_group
        }

        serializer = CompanyGroupMemberPostSerializer(company_group_member, data=request.DATA)
        if serializer.is_valid():
            serializer.save()

            # Collect updated group information and send notfiication email
            updated_company_group_member = self._get_object(pk)
            group_member_change_info['updated_company_group'] = updated_company_group_member.company_group
            self._send_notification_email(group_member_change_info)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        group_member = self._get_object(pk)
        group_member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _send_notification_email(self, group_member_change_info):
        send_email_service = SendEmailService()

        subject = 'Employee Benefit Group Change Notification'
        html_template_path = 'email/employee_benefit_group_change_notification.html'
        txt_template_path = 'email/employee_benefit_group_change_notification.txt'

        # build the list of target emails
        to_emails = send_email_service.get_broker_emails_by_company(group_member_change_info['company'].id)

        # get person data from user
        group_member_change_info['person'] = group_member_change_info['user'].family.filter(relationship=SELF).first()
        if (not group_member_change_info['person']):
            # Use the user information if the account does not have person profile
            # setup
            group_member_change_info['person'] = group_member_change_info['user']

        # build the template context data
        context_data = send_email_service.get_base_email_context_data()
        context_data['group_member_change_info'] = group_member_change_info

        # get PDF
        pdf_service = CompanyEmployeeBenefitPdfReportService()
        pdf_buffer = StringIO()
        pdf_service.get_employee_report(
            group_member_change_info['user'].id,
            group_member_change_info['company'].id,
            pdf_buffer)
        pdf = pdf_buffer.getvalue()
        pdf_buffer.close()

        send_email_service.send_support_email(
            to_emails, subject, context_data, html_template_path, txt_template_path,
            attachment_name='employee_details.pdf', attachment=pdf, attachment_mime_type='application/pdf')

        return


class CompanyGroupMemberCompanyGroupView(APIView):
    def get(self, request, pk, format=None):
        group_members = CompanyGroupMember.objects.filter(company_group=pk)
        serializer = CompanyGroupMemberSerializer(group_members, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        serializer = CompanyGroupMemberPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CompanyGroupMemberCompanyView(APIView):
    def get(self, request, pk, format=None):
        groups = CompanyGroup.objects.filter(company=pk)
        serializer = CompanyGroupWithMemberSerializer(groups, many=True)
        return Response(serializer.data)
