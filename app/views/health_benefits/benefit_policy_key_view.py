from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from app.models.health_benefits.benefit_policy_key import BenefitPolicyKey
from app.serializers.health_benefits.benefit_policy_key_serializer import BenefitPolicyKeySerializer

class BenefitPolicyKeyView(APIView):
    def get(self, request, format=None):
        entries = BenefitPolicyKey.objects.all().order_by('rank')
        serialized = BenefitPolicyKeySerializer(entries, many=True)
        return Response(serialized.data)
