from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from app.models.company_group import CompanyGroup
from app.models.company_group_member import CompanyGroupMember 
from app.serializers.company_group_member_serializer import (
    CompanyGroupMemberSerializer,
    CompanyGroupMemberPostSerializer)


class CompanyGroupMemberView(APIView):
    def _get_object(self, pk):
        try:
            return CompanyGroupMember.objects.get(pk=pk)
        except CompanyGroupMember.DoesNotExist:
            raise Http404

    def post(self, request, pk, format=None):
        serializer = CompanyGroupMemberPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        company_group_member = self._get_object(pk)
        serializer = CompanyGroupPostSerializer(company_group_member, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
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


class CompanyGroupMemberCompanyView(APIView):
    def get(self, request, pk, format=None):
        members = []
        groups = CompanyGroup.objects.filter(company=pk)
        for group in groups:
            members.extend(group.company_group_member.all())
        serializer = CompanyGroupMemberSerializer(members, many=True)
        return Response(serializer.data)
