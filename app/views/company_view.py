from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.http import Http404
from django.contrib.auth import get_user_model

from app.models.company_user import CompanyUser
from app.models.company import Company
from app.models.company_group import CompanyGroup
from app.serializers.company_serializer import (
    CompanySerializer,
    CompanyPostSerializer)

User = get_user_model()

class CompanyView(APIView):
    def get_object(self, pk):
        try:
            return Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        company = self.get_object(pk)
        serializer = CompanySerializer(company)
        return Response(serializer.data)

    @transaction.atomic
    def put(self, request, pk, format=None):
        company = self.get_object(pk)
        serializer = CompanyPostSerializer(company, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def post(self, request, format=None):
        # We first need to create an active user for it
        contact_size = len(request.DATA['contacts'])
        u = None

        if contact_size:
            primary_contact = request.DATA['contacts'][0]
            u = User.objects.create_user(primary_contact['email'], primary_contact.get('password', 'temp'))
            if u and primary_contact['first_name'] and primary_contact['last_name']:
                u.first_name = primary_contact['first_name']
                u.last_name = primary_contact['last_name']

            u.save()
            primary_contact['relationship'] = 'self'
            primary_contact['user'] = u.id

        serializer = CompanyPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            if u:
                company_user = CompanyUser(user_id = u.id,
                                           company=serializer.object,
                                           company_user_type="admin")
                company_user.save()

            broker_user = CompanyUser(user_id=request.user.pk,
                                       company=serializer.object,
                                       company_user_type="broker")
            broker_user.save()

            if request.DATA['default_benefit_groups']:
                groups = request.DATA['default_benefit_groups']
                for group in groups:
                    company_group = CompanyGroup(name=group, company=serializer.object)
                    company_group.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
