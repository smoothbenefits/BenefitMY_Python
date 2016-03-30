from datetime import datetime
from trigger_no_work_time_tracking_base import TriggerNoWorkTimeTrackingBase

# Weekday 6 is Sunday
NOTIFICATION_WEEKDAY = 6


class TriggerEmployeeNoWorkTimeTracking(TriggerNoWorkTimeTrackingBase):
    def __init__(self):
        super(TriggerEmployeeNoWorkTimeTracking, self).__init__()

    def _check_schedule(self):
        weekday = datetime.now().weekday()
        return weekday == NOTIFICATION_WEEKDAY
