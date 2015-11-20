from triggers.trigger_employee_not_complete_enrollment \
    import TriggerEmployeeNotCompleteEnrollment
from triggers.trigger_company_not_complete_emrollment \
    import TriggerCompanyNotCompleteEnrollment
from actions.action_notify_employee_not_complete_enrollment \
    import ActionNotifyEmployeeNotCompleteEnrollment
from actions.action_notify_company_not_complete_enrollment \
    import ActionNotifyCompanyNotCompleteEnrollment
from actions.action_print_to_console import ActionPrintToConsole


''' Provides a facility to manage and deliver system notifactions
    to the intended parties.
'''
class NotificationService(object):
    def __init__(self):
        # Initialize all the trigger to action links here
        # This can potentially be exposed to consumers of
        # the service, but don't see the need to delegate
        # this now.
        self._triggers = []

        trig_emp_not_enroll = TriggerEmployeeNotCompleteEnrollment()
        # trig_emp_not_enroll.append_action(ActionPrintToConsole())
        trig_emp_not_enroll.append_action(ActionNotifyEmployeeNotCompleteEnrollment())
        self._triggers.append(trig_emp_not_enroll)

        trig_comp_not_enroll = TriggerCompanyNotCompleteEnrollment()
        # trig_comp_not_enroll.append_action(ActionPrintToConsole())
        trig_comp_not_enroll.append_action(ActionNotifyCompanyNotCompleteEnrollment())
        self._triggers.append(trig_comp_not_enroll)

    def execute(self):
        for trigger in self._triggers:
            trigger.examine_and_execute_actions()
