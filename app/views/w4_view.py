from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from app.models.w4 import W4
from app.serializers.w4_serializer import W4Serializer

from app.service.event_bus.aws_event_bus_service import AwsEventBusService
from app.service.event_bus.events.w4_updated_event import W4UpdatedEvent


class W4View(APIView):
    _aws_event_bus_service = AwsEventBusService()

    def _get_object(self, pk):
        try:
            return W4.objects.get(user=pk)
        except W4.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        w4 = self._get_object(pk)
        serializer = W4Serializer(w4)
        return Response(serializer.data)


    @transaction.atomic
    def post(self, request, pk, format=None):

        request.DATA['user'] = pk
        try:
            w4 = W4.objects.get(user=pk)
            serializer = W4Serializer(w4,
                                      data=request.DATA)
            if serializer.is_valid():
                serializer.save()

                # Log event
                self._aws_event_bus_service.publish_event(W4UpdatedEvent(pk))

                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except W4.DoesNotExist:
            serializer = W4Serializer(data=request.DATA)
            if serializer.is_valid():
                serializer.save()

                # Log event
                self._aws_event_bus_service.publish_event(W4UpdatedEvent(pk))
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
