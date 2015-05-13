from rest_framework.views import APIView
from rest_framework.response import Response

from app.models.sys_suppl_life_insurance_condition import SysSupplLifeInsuranceCondition
from app.serializers.sys_suppl_life_insurance_condition_serializer import \
    SysSupplLifeInsuranceConditionSerializer

class SysSupplementalLifeInsuranceConditionView(APIView):

    def get(self, request, format=None):
        conditions = SysSupplLifeInsuranceCondition.objects.all()
        serialized = SysSupplLifeInsuranceConditionSerializer(conditions, many=True)
        return Response(serialized.data)
