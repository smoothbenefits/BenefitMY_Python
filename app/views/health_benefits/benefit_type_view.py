from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response

from app.models.health_benefits.benefit_type import BenefitType
from app.serializers.health_benefits.benefit_type_serializer import BenefitTypeSerializer


class BenefitTypeView(APIView):

    def get(self, request, format=None):
        types = BenefitType.objects.all()
        serializer = BenefitTypeSerializer(types, many=True)
        return Response({'benefit_types': serializer.data})
