from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from app.models.sys_application_feature import SysApplicationFeature
from app.serializers.sys_application_feature_serializer import SysApplicationFeatureSerializer

class SysApplicationFeatureView(APIView):
    def get(self, request, format=None):
        features = SysApplicationFeature.objects.all()
        serialized = SysApplicationFeatureSerializer(features, many=True)
        return Response(serialized.data)
