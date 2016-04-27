from ...trigger_base import TriggerBase
from app.service.hash_key_service import HashKeyService
from app.service.send_email_service import SendEmailService


class TriggerCoiExpirationCheck(TriggerBase):
    def __init__(self):
        super(TriggerCoiExpirationCheck, self).__init__()

    def _examine_condition(self):
        # For now, this just rely on the outer (cron job)
        # schedule
        return True

    def _get_action_data(self):
        hash_key_service = HashKeyService()
        send_email_service = SendEmailService()
        company_emails = send_email_service.get_employer_emails_for_all_companies()

        result = []

        for companyId in company_emails.keys():
            result.append({
                'descriptor': hash_key_service.encode_key_with_environment(companyId),
                'emailList': company_emails[companyId]
            })

        return result
