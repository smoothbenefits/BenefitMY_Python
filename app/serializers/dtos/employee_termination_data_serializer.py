from rest_framework import serializers
from app.dtos.employee_termination_data import EmployeeTerminationData


class EmployeeTerminationDataSerializer(serializers.Serializer):
    person_id = serializers.IntegerField()
    company_id = serializers.IntegerField()
    end_date = serializers.DateField()

    def restore_object(self, attrs, instance=None):
        return EmployeeTerminationData(**attrs)
