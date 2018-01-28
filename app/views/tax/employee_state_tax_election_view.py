from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from app.models.tax.employee_state_tax_election import EmployeeStateTaxElection
from app.service.monitoring.logging_service import LoggingService
from app.service.event_bus.aws_event_bus_service import AwsEventBusService
from app.service.event_bus.events.state_tax_updated_event import StateTaxUpdatedEvent
from app.serializers.tax.employee_state_tax_election_serializer_factory import EmployeeStateTaxElectionSerializerFactory


class EmployeeStateTaxElectionView(APIView):
    _aws_event_bus_service = AwsEventBusService()
    _state_tax_election_serializer_factory = EmployeeStateTaxElectionSerializerFactory()

    def _get_object(self, user_id, state, require_exist=True):
        try:
            return EmployeeStateTaxElection.objects.get(user=user_id, state=state)
        except EmployeeStateTaxElection.DoesNotExist:
            if (require_exist):
                raise Http404
            else:
                return None

    def get(self, request, user_id, state, format=None):
        record = self._get_object(user_id, state)

        # Below is to handle the case where the tax record was imported, and hence
        # requires the special serializer to handle
        imported = (record.tax_election_data and record.tax_election_data.is_imported)
        if (imported):
            raise Http404

        serializer = self._state_tax_election_serializer_factory.get_employee_state_tax_election_serializer(state)(record)
        return Response(serializer.data)

    def delete(self, request, user_id, state, format=None):
        record = self._get_object(user_id, state)
        record.delete()

        # Log event
        self._aws_event_bus_service.publish_event(StateTaxUpdatedEvent(user_id, state))
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, user_id, state, format=None):
        record = self._get_object(user_id, state)
        serializer = self._state_tax_election_serializer_factory.get_employee_state_tax_election_post_serializer(state)(record, data=request.DATA)
        if serializer.is_valid():
            serializer.save()

            # Log event
            self._aws_event_bus_service.publish_event(StateTaxUpdatedEvent(user_id, state))

            response_serializer = self._state_tax_election_serializer_factory.get_employee_state_tax_election_serializer(state)(serializer.object)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, user_id, state, format=None):
        record = self._get_object(user_id, state, require_exist=False)

        serializer = None
        if (record):
            serializer = self._state_tax_election_serializer_factory.get_employee_state_tax_election_post_serializer(state)(record, data=request.DATA)
        else:
            serializer = self._state_tax_election_serializer_factory.get_employee_state_tax_election_post_serializer(state)(data=request.DATA)
        
        if serializer.is_valid():
            serializer.save()
            record = serializer.object

            # Log event
            self._aws_event_bus_service.publish_event(StateTaxUpdatedEvent(user_id, state))

            response_serializer = self._state_tax_election_serializer_factory.get_employee_state_tax_election_serializer(state)(record)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeStateTaxElectionByEmployeeView(APIView):
    _state_tax_election_serializer_factory = EmployeeStateTaxElectionSerializerFactory()

    def _get_object_collection(self, user_id):
        return EmployeeStateTaxElection.objects.filter(user=user_id)

    def get(self, request, user_id, format=None):
        records = self._get_object_collection(user_id)
        result = []
        for record in records:
            # Below is to handle the case where the tax record was imported
            # for not the treatment is to ignore such record, so that to clients,
            # these records would be just non-existent.
            imported = (record.tax_election_data and record.tax_election_data.is_imported)
            if imported:
                continue

            serializer = self._state_tax_election_serializer_factory.get_employee_state_tax_election_serializer(record.state)(record)
            result.append(serializer.data)
        return Response(result)
