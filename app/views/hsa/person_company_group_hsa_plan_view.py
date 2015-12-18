from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from app.models.hsa.person_company_group_hsa_plan import PersonCompanyGroupHsaPlan
from app.serializers.hsa.person_company_group_hsa_plan_serializer import \
    (PersonCompanyGroupHsaPlanSerializer, PersonCompanyGroupHsaPlanPostSerializer)

class PersonCompanyGroupHsaPlanView(APIView):

    def _get_object(self, person_id):
        try:
            return PersonCompanyGroupHsaPlan.objects.filter(person=person_id)
        except PersonCompanyGroupHsaPlan.DoesNotExist:
            raise Http404

    def get(self, request, person_id, format=None):
        person_hsa = self._get_object(person_id)
        serializer = PersonCompanyGroupHsaPlanSerializer(person_hsa, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        serializer = PersonCompanyGroupHsaPlanPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        person_hsa = self._get_object(pk)
        serializer = PersonCompanyGroupHsaPlanPostSerializer(person_hsa, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        person_hsa = self._get_object(pk)
        person_hsa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
