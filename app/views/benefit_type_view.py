from rest_framework.views import APIView
from rest_framework.response import Response

from app.models.benefit_type import BenefitType
from app.serializers.benefit_type_serializer import BenefitTypeSerializer
from view_mixin import *


class BenefitTypeView(APIView, LoginRequiredMixin):

    def get(self, request, format=None):
        types = BenefitType.objects.all()
        serializer = BenefitTypeSerializer(types, many=True)
        return Response({'benefit_types': serializer.data})
