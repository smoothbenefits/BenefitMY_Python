from app.service.hash_key_service import HashKeyService
from app.serializers.sys_compensation_update_reason_serializer import SysCompensationUpdateReasonSerializer

class CompensationInfo(object):
    id = None
    effective_date = None
    annual_base_salary = None
    hourly_rate = None
    increase_percentage = None
    projected_hour_per_month = None
    created_at = None
    updated_at = None
    is_current = False
    reason = None

    def __init__(self, compensation_record):
        self.key_hasher = HashKeyService()
        if compensation_record:
            self.id = self.key_hasher.encode_key(compensation_record.id)
            self.effective_date = compensation_record.effective_date
            self.annual_base_salary = compensation_record.annual_base_salary
            self.hourly_rate = compensation_record.hourly_rate
            self.increase_percentage = compensation_record.increase_percentage
            self.projected_hour_per_month = compensation_record.projected_hour_per_month
            self.created_at = compensation_record.created_at
            self.updated_at = compensation_record.updated_at
            self.reason = compensation_record.reason

    def __cmp__(self, other):
        if hasattr(other, 'effective_date'):
            return self.effective_date.__cmp__(other.effective_date)
