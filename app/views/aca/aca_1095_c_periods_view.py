from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from app.models.aca.company_1095_c import PERIODS

class ACA1095CPeriodsView(APIView):
    def get(self, request, format=None):
        return Response(PERIODS)
