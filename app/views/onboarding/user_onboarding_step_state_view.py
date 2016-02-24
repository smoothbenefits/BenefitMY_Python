from django.db import transaction
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app.models.onboarding.user_onboarding_step_state \
    import UserOnboardingStepState
from app.serializers.onboarding.user_onboarding_step_state_serializer \
    import (
        UserOnboardingStepStateSerializer,
        UserOnboardingStepStatePostSerializer
    )


class UserOnboardingStepStateView(APIView):
    def _get_object(self, pk):
        try:
            return UserOnboardingStepState.objects.get(pk=pk)
        except UserOnboardingStepState.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        entry = self._get_object(pk)
        serializer = UserOnboardingStepStateSerializer(entry)
        return Response(serializer.data)

    @transaction.atomic
    def delete(self, request, pk, format=None):
        entry = self._get_object(pk)
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    def put(self, request, pk, format=None):
        entry = self._get_object(pk)
        serializer = UserOnboardingStepStatePostSerializer(entry, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def post(self, request, format=None):
        serializer = UserOnboardingStepStatePostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserOnboardingStepStateByUserView(APIView):

    def get(self, request, pk, format=None):
        entries = UserOnboardingStepState.objects.filter(user=pk)
        serializer = UserOnboardingStepStateSerializer(entries, many=True)
        return Response(serializer.data)
