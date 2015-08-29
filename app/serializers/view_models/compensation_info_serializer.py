from rest_framework import serializers
from app.serializers.sys_compensation_update_reason_serializer import SysCompensationUpdateReasonSerializer
from app.view_models.compensation_info import CompensationInfo

class CompensationInfoSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    effective_date = serializers.DateTimeField()
    annual_base_salary = serializers.DecimalField(max_digits=12,
                                                  decimal_places=2,
                                                  required=False)
    hourly_rate = serializers.DecimalField(max_digits=12, 
                                            decimal_places=4,
                                            required=False)
    increase_percentage = serializers.DecimalField(max_digits=5,
                                              decimal_places=2,
                                              required=False)
    projected_hour_per_month = serializers.DecimalField(max_digits=12, 
                                                    decimal_places=4,
                                                    required=False)
    created_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)
    is_current = serializers.BooleanField(required=False)
    reason = SysCompensationUpdateReasonSerializer(required=False)

    def restore_object(self, attrs, instance=None):
        return CompensationInfo(**attrs)
