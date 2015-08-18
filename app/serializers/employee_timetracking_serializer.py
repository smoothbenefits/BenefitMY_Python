from rest_framework import serializers
from app.models.employee_timetracking import EmployeeTimeTracking
from hash_pk_serializer_base import HashPkSerializerBase
from custom_fields.hash_field import HashField

class EmployeeTimeTrackingSerializer(HashPkSerializerBase):
    person = HashField(source="person.id")
    company = HashField(source="company.id")
    class Meta:
        model = EmployeeTimeTracking

class EmployeeTimeTrackingPostSerializer(HashPkSerializerBase):
    class Meta:
        model = EmployeeTimeTracking
