from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from app.models.tax.employee_state_tax_election import EmployeeStateTaxElection
from app.service.monitoring.logging_service import LoggingService
from app.service.event_bus.aws_event_bus_service import AwsEventBusService
from app.serializers.tax.employee_state_tax_election_serializer_factory import EmployeeStateTaxElectionSerializerFactory


class EmployeeStateTaxElectionView(APIView):
    _aws_event_bus_service = AwsEventBusService()
    _state_tax_election_serializer_factory = EmployeeStateTaxElectionSerializerFactory()

    def _get_object(self, user_id, state):
        try:
            return EmployeeStateTaxElection.objects.get(user=user_id, state=state)
        except EmployeeStateTaxElection.DoesNotExist:
            raise Http404

    def get(self, request, user_id, state, format=None):
        record = self._get_object(user_id, state)
        serializer = self._state_tax_election_serializer_factory.get_employee_state_tax_election_serializer(state)(record)
        return Response(serializer.data)

    def delete(self, request, user_id, state, format=None):
        record = self._get_object(user_id, state)
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, user_id, state, format=None):
        record = self._get_object(user_id, state)
        serializer = self._state_tax_election_serializer_factory.get_employee_state_tax_election_post_serializer(state)(record, data=request.DATA)
        if serializer.is_valid():
            serializer.save()

            # TODO: Log event here

            response_serializer = self._state_tax_election_serializer_factory.get_employee_state_tax_election_serializer(state)(serializer.object)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, user_id, state, format=None):
        serializer = self._state_tax_election_serializer_factory.get_employee_state_tax_election_post_serializer(state)(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            record = serializer.object

            # TODO: log event here

            response_serializer = self._state_tax_election_serializer_factory.get_employee_state_tax_election_serializer(state)(record)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
