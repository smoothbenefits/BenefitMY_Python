from rest_framework import serializers
from app.serializers.sys_compensation_update_reason_serializer import SysCompensationUpdateReasonSerializer


class CompensationInfoSerializer(serializers.Serializer):
    id = serializers.CharField()
    effective_date = serializers.DateTimeField()
    annual_base_salary = serializers.DecimalField(max_digits=12,
                                                  decimal_places=2)
    hourly_rate = serializers.DecimalField(max_digits=12, decimal_places=4)
    increase_percentage = serializers.DecimalField(max_digits=5,
                                              decimal_places=2)
    projected_hour_per_month = serializers.DecimalField(max_digits=12, decimal_places=4)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    is_current = serializers.BooleanField()
    reason = SysCompensationUpdateReasonSerializer()
