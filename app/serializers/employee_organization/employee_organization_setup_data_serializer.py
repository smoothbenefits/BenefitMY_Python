from rest_framework import serializers
from app.dtos.employee_organization.employee_organization_setup_data \
    import EmployeeOrganizationSetupData
from app.serializers.person_serializer import PersonSimpleSerializer
from app.serializers.employee_profile_serializer import ManagerSerializer


''' Deserialize data corresponding to one complete data object
    expected to carry out a unit the employee organization setup
    operation. 
'''
class EmployeeOrganizationSetupDataPostSerializer(serializers.Serializer):
    employee_person_id = serializers.IntegerField(required=False)
    employee_first_name = serializers.CharField(required=False)
    employee_last_name = serializers.CharField(required=False)
    company_id = serializers.IntegerField()
    manager_profile_id = serializers.IntegerField(required=False)
    manager_first_name = serializers.CharField(required=False)
    manager_last_name = serializers.CharField(required=False)

    def restore_object(self, attrs, instance=None):
        return EmployeeOrganizationSetupData(**attrs)


''' Serailize out data object that holds the data expected to carry
    out a unit the employee organization setup operation.
'''
class EmployeeOrganizationSetupDataSerializer(serializers.Serializer):
    employee_person_id = serializers.IntegerField(required=False)
    employee_first_name = serializers.CharField(required=False)
    employee_last_name = serializers.CharField(required=False)
    company_id = serializers.IntegerField()
    manager_profile_id = serializers.IntegerField(required=False)
    manager_first_name = serializers.CharField(required=False)
    manager_last_name = serializers.CharField(required=False)

    employee_person_info = PersonSimpleSerializer(source="get_employee_person")
    manager_profile_info = ManagerSerializer(source="get_manager_profile")
