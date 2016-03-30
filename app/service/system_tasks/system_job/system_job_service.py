from ..action_print_to_console import ActionPrintToConsole
from ..system_task_service_base import SystemTaskServiceBase
from triggers.trigger_timeoff_accrual import TriggerTimeoffAccrual
from actions.action_timeoff_accrual import ActionTimeoffAccural


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
