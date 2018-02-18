from triggers.trigger_employee_not_complete_enrollment \
    import TriggerEmployeeNotCompleteEnrollment
from triggers.trigger_employee_not_sign_document \
    import TriggerEmployeeNotSignDocument
from triggers.trigger_company_not_complete_emrollment \
    import TriggerCompanyNotCompleteEnrollment
from triggers.trigger_company_not_sign_document \
    import TriggerCompanyNotSignDocument
from triggers.trigger_employee_no_work_time_tracking \
    import TriggerEmployeeNoWorkTimeTracking
from triggers.trigger_employee_i9_expiration \
    import TriggerEmployeeI9Expiration
from triggers.trigger_company_not_complete_onboarding \
    import TriggerCompanyNotCompleteOnboarding
from triggers.trigger_employee_not_complete_onboarding \
    import TriggerEmployeeNotCompleteOnboarding
from actions.action_notify_employee_not_complete_enrollment \
    import ActionNotifyEmployeeNotCompleteEnrollment
from actions.action_notify_employee_not_sign_document \
    import ActionNotifyEmployeeNotSignDocument
from actions.action_notify_company_not_complete_enrollment \
    import ActionNotifyCompanyNotCompleteEnrollment
from actions.action_notify_company_not_sign_document \
    import ActionNotifyCompanyNotSignDocument
from actions.action_notify_employee_no_work_time_tracking \
    import ActionNotifyEmployeeNoWorkTimeTracking
from actions.action_notify_company_i9_expiration \
    import ActionNotifyCompanyI9Expiration
from actions.action_notify_company_not_complete_onboarding \
    import ActionNotifyCompanyNotCompleteOnboarding
from actions.action_notify_employee_not_complete_onboarding \
    import ActionNotifyEmployeeNotCompleteOnboarding
from ..action_print_to_console import ActionPrintToConsole
from ..system_task_service_base import SystemTaskServiceBase


''' Provides a facility to manage and deliver system notifactions
    to the intended parties.
'''
class NotificationService(SystemTaskServiceBase):
    def __init__(self):
        super(NotificationService, self).__init__()

        trig_emp_not_enroll = TriggerEmployeeNotCompleteEnrollment()
        trig_emp_not_enroll.append_action(ActionNotifyEmployeeNotCompleteEnrollment())
        self.register_trigger(trig_emp_not_enroll)

        trig_comp_not_enroll = TriggerCompanyNotCompleteEnrollment()
        trig_comp_not_enroll.append_action(ActionNotifyCompanyNotCompleteEnrollment())
        self.register_trigger(trig_comp_not_enroll)

        trig_emp_not_onboard = TriggerEmployeeNotCompleteOnboarding()
        trig_emp_not_onboard.append_action(ActionNotifyEmployeeNotCompleteOnboarding())
        self.register_trigger(trig_emp_not_onboard)

        trig_comp_not_onboard = TriggerCompanyNotCompleteOnboarding()
        trig_comp_not_onboard.append_action(ActionNotifyCompanyNotCompleteOnboarding())
        self.register_trigger(trig_comp_not_onboard)

        trig_emp_not_sign_doc = TriggerEmployeeNotSignDocument()
        trig_emp_not_sign_doc.append_action(ActionNotifyEmployeeNotSignDocument())
        self.register_trigger(trig_emp_not_sign_doc)

        trig_comp_not_sign_document = TriggerCompanyNotSignDocument()
        trig_comp_not_sign_document.append_action(ActionNotifyCompanyNotSignDocument())
        self.register_trigger(trig_comp_not_sign_document)

        trig_emp_no_work_time_tracking = TriggerEmployeeNoWorkTimeTracking()
        trig_emp_no_work_time_tracking.append_action(ActionNotifyEmployeeNoWorkTimeTracking())
        self.register_trigger(trig_emp_no_work_time_tracking)

        trig_employee_i9_expiration = TriggerEmployeeI9Expiration()
        trig_employee_i9_expiration.append_action(ActionNotifyCompanyI9Expiration())
        self.register_trigger(trig_employee_i9_expiration)
