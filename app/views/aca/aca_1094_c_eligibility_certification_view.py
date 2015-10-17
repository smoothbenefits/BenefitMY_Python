from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from app.models.aca.company_1094_c_member_info import ELIGIBILITY_CERTIFICATIONS

class ACA1094CEligibilityCertificationView(APIView):
    def get(self, request, format=None):
        return Response(ELIGIBILITY_CERTIFICATIONS)
