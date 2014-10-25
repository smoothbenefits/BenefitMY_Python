from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response

from app.models.company_user import CompanyUser
from app.serializers.user_company_roles_serializer import UserCompanyRolesSerializer


class UserCompanyRolesView(APIView):
    def get_companies(self, pk):
        try:
            return CompanyUser.objects.filter(user=pk)
        except CompanyUser.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        companies = self.get_companies(pk)
        serializer = UserCompanyRolesSerializer(companies, many=True)
        return Response(serializer.data)
