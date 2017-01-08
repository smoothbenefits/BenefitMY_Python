from django.conf import settings
from django.contrib.auth import get_user_model

from app.service.hash_key_service import HashKeyService
from app.service.web_request_service import WebRequestService

from app.view_models.time_tracking.time_punch_card import TimePunchCard
from app.view_models.time_tracking.reported_hours import ReportedHours

User = get_user_model()

# Time Punch Card Types
PUNCH_CARD_TYPE_WORK_TIME = 'Work Time'
PUNCH_CARD_TYPE_COMPANY_HOLIDAY = 'Company Holiday'
PUNCH_CARD_TYPE_PAID_TIME_OFF = 'Paid Time Off'
PUNCH_CARD_TYPE_SICK_TIME = 'Sick Time'
PUNCH_CARD_TYPE_PERSONAL_LEAVE = 'Personal Leave'


class TimePunchCardService(object):

    hash_key_service = HashKeyService()
    request_service = WebRequestService()

    def get_company_users_time_punch_cards_by_date_range(
        self,
        company_id,
        start_date,
        end_date
    ):
        user_punch_cards = []
        api_url = '{0}api/v1/company/{1}/time_punch_cards?start_date={2}&end_date={3}'.format(
            settings.TIME_TRACKING_SERVICE_URL,
            self.hash_key_service.encode_key_with_environment(company_id),
            start_date.isoformat(),
            end_date.isoformat())

        r = self.request_service.get(api_url)
        if r.status_code == 404:
            return user_punch_cards

        all_entries = r.json()
        for entry in all_entries:
            user_punch_cards.append(TimePunchCard(entry))

        return user_punch_cards

    def get_company_users_reported_hours_by_date_range(
        self,
        company_id,
        start_date,
        end_date
    ):
        user_punch_cards = self.get_company_users_time_punch_cards_by_date_range(
                company_id,
                start_date,
                end_date)

        result_dict = {}

        for card in user_punch_cards:
            if (card.user_id not in result_dict):
                result_dict[card.user_id] = ReportedHours()

            if (card.card_type == PUNCH_CARD_TYPE_PERSONAL_LEAVE):
                result_dict[card.user_id].unpaid_hours += card.get_punch_card_hours()
            else:
                result_dict[card.user_id].paid_hours += card.get_punch_card_hours()

        return result_dict
