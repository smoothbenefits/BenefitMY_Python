from rest_framework import serializers
from app.dtos.employee_organization.batch_employee_organization_import_raw_data \
    import BatchEmployeeOrganizationImportRawData


class BatchEmployeeOrganizationImportRawDataSerializer(serializers.Serializer):
    raw_data = serializers.CharField()

    def restore_object(self, attrs, instance=None):
        return BatchEmployeeOrganizationImportRawData(**attrs)
