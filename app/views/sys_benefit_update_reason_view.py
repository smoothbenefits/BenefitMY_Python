from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from app.models.sys_benefit_update_reason import SysBenefitUpdateReason
from app.serializers.sys_benefit_update_reason_serializer import SysBenefitUpdateReasonSerializer

class SysBenefitUpdateReasonView(APIView):
    def get(self, request, format=None):
        reasons = SysBenefitUpdateReason.objects.all()
        serialized = SysBenefitUpdateReasonSerializer(reasons, many=True)
        return Response(serialized.data)
