from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response

from app.models.user import User
from app.models.company_user import CompanyUser
from app.serializers.company_user_serializer import CompanyUserSerializer


class CompanyUsersView(APIView):
    def get_companies(self, pk):
        try:
            return CompanyUser.objects.filter(company=pk)
        except CompanyUser.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        companies = self.get_companies(pk)
        serializer = CompanyUserSerializer(companies, many=True)
        return Response(serializer.data)
