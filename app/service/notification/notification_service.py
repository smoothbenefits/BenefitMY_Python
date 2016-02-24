from triggers.trigger_employee_not_complete_enrollment \
    import TriggerEmployeeNotCompleteEnrollment
from triggers.trigger_employee_not_sign_document \
    import TriggerEmployeeNotSignDocument
from triggers.trigger_company_not_complete_emrollment \
    import TriggerCompanyNotCompleteEnrollment
from triggers.trigger_company_not_sign_document \
    import TriggerCompanyNotSignDocument
from actions.action_notify_employee_not_complete_enrollment \
    import ActionNotifyEmployeeNotCompleteEnrollment
from actions.action_notify_employee_not_sign_document \
    import ActionNotifyEmployeeNotSignDocument
from actions.action_notify_company_not_complete_enrollment \
    import ActionNotifyCompanyNotCompleteEnrollment
from actions.action_notify_company_not_sign_document \
    import ActionNotifyCompanyNotSignDocument
from actions.action_print_to_console import ActionPrintToConsole
from ..monitoring.logging_service import LoggingService

log = LoggingService()

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
        trig_emp_not_enroll.append_action(ActionNotifyEmployeeNotCompleteEnrollment())
        self._triggers.append(trig_emp_not_enroll)

        trig_comp_not_enroll = TriggerCompanyNotCompleteEnrollment()
        trig_comp_not_enroll.append_action(ActionNotifyCompanyNotCompleteEnrollment())
        self._triggers.append(trig_comp_not_enroll)

        trig_emp_not_sign_doc = TriggerEmployeeNotSignDocument()
        trig_emp_not_sign_doc.append_action(ActionNotifyEmployeeNotSignDocument())
        self._triggers.append(trig_emp_not_sign_doc)

        trig_comp_not_sign_document = TriggerCompanyNotSignDocument()
        trig_comp_not_sign_document.append_action(ActionNotifyCompanyNotSignDocument())
        self._triggers.append(trig_comp_not_sign_document)

    def execute(self):
        for trigger in self._triggers:
            trigger.examine_and_execute_actions()
            log.info("Finished trigger {}".format(type(trigger).__name__))
