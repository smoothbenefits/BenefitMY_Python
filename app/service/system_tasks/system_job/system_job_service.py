from ..action_print_to_console import ActionPrintToConsole
from ..system_task_service_base import SystemTaskServiceBase
from triggers.trigger_timeoff_accrual import TriggerTimeoffAccrual
from actions.action_timeoff_accrual import ActionTimeoffAccural
from triggers.trigger_coi_expiration_check import TriggerCoiExpirationCheck
from actions.action_coi_expiration_check import ActionCoiExpirationCheck

''' Provides a facility to manage and deliver system notifactions
    to the intended parties.
'''
class SystemJobService(SystemTaskServiceBase):
    def __init__(self):
        super(SystemJobService, self).__init__()

        # Timeoff accrual
        trig_timeoff_accrual = TriggerTimeoffAccrual()
        trig_timeoff_accrual.append_action(ActionTimeoffAccural())
        self.register_trigger(trig_timeoff_accrual)

        # COI expiration validation
        trig_coi_expire_check = TriggerCoiExpirationCheck()
        trig_coi_expire_check.append_action(ActionCoiExpirationCheck())
        self.register_trigger(trig_coi_expire_check)
