from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from app.models.workers_comp.employee_phraseology import \
    EmployeePhraseology
from app.serializers.workers_comp.employee_phraseology_serializer import (
    EmployeePhraseologySerializer,
    EmployeePhraseologyPostSerializer)


class EmployeePhraseologyView(APIView):
    def _get_object(self, pk):
        try:
            return EmployeePhraseology.objects.get(pk=pk)
        except EmployeePhraseology.DoesNotExist:
            raise Http404

    def _get_current_phraseology_by_employee_person(self, person_id):
        # Wrapping in a list to force evaluation
        return list(EmployeePhraseology.objects.filter(
            employee_person=person_id, end_date__isnull=True))

    def get(self, request, pk, format=None):
        model = self._get_object(pk)
        serializer = EmployeePhraseologySerializer(model)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        model = self._get_object(pk)
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        model = self._get_object(pk)
        serializer = EmployeePhraseologyPostSerializer(model, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def post(self, request, format=None):
        serializer = EmployeePhraseologyPostSerializer(data=request.DATA)
        if serializer.is_valid():
            # First find current employee phraseology, if one exists
            # This needs to be collect before saving the new model
            # or else the new model will be included in this result set
            current_phraseologys = self._get_current_phraseology_by_employee_person(
                serializer.object.employee_person.id)

            # Save the new posted data, to create the model
            serializer.save()

            # Now update existing current entry to mark its end_date
            for entry in current_phraseologys:
                entry.end_date = serializer.object.start_date
                entry.save()

            response_serializer = EmployeePhraseologySerializer(serializer.object)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeePhraseologyByEmployeePersonView(APIView):
    def _get_object(self, person_id):
        return EmployeePhraseology.objects.filter(employee_person=person_id)

    def get(self, request, person_id, format=None):
        models = self._get_object(person_id)
        serializer = EmployeePhraseologySerializer(models, many=True)
        return Response(serializer.data)
