from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from app.models.company_user import CompanyUser
from app.serializers.company_user_serializer import (
    CompanyUserSerializer,
    CompanyUserPostSerializer)


class CompanyUserView(APIView):
    def get_companies(self, pk):
        try:
            return CompanyUser.objects.filter(company=pk)
        except CompanyUser.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        companies = self.get_companies(pk)
        serializer = CompanyUserSerializer(companies, many=True)
        return Response({'user_roles':serializer.data})


@api_view(['POST'])
def company_user(request, pk):
    serializer = CompanyUserPostSerializer(data=request.DATA)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
