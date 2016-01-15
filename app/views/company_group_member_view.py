from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from app.models.company_group import CompanyGroup
from app.models.company_group_member import CompanyGroupMember 
from app.models.person import Person
from app.serializers.company_group_member_serializer import (
    CompanyGroupMemberSerializer,
    CompanyGroupMemberPostSerializer,
    CompanyGroupWithMemberSerializer)
from app.service.send_email_service import SendEmailService


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
        original_group = company_group_member.company_group

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
            email_service = SendEmailService()
            email_service.send_employee_benefit_group_update_notification_email(
                company_group_member.user, 
                company_group_member.company_group.company,
                original_group,
                updated_company_group_member.company_group
            )

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        group_member = self._get_object(pk)
        group_member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
