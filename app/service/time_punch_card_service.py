from datetime import timedelta
from django.conf import settings
from django.contrib.auth import get_user_model

from app.service.hash_key_service import HashKeyService
from app.service.web_request_service import WebRequestService
from app.service.application_feature_service import (
    APP_FEATURE_HOLIDAYSASWORKINGHOURS,
    ApplicationFeatureService
)

from app.view_models.time_tracking.time_punch_card import TimePunchCard
from app.view_models.time_tracking.reported_hours import ReportedHours
from app.view_models.time_tracking.employee_daily_punch_card_aggregate import EmployeeDailyPunchCardAggregate

User = get_user_model()

# Time Punch Card Types
PUNCH_CARD_TYPE_WORK_TIME = 'Work Time'
PUNCH_CARD_TYPE_COMPANY_HOLIDAY = 'Company Holiday'
PUNCH_CARD_TYPE_PAID_TIME_OFF = 'Paid Time Off'
PUNCH_CARD_TYPE_SICK_TIME = 'Sick Time'
PUNCH_CARD_TYPE_PERSONAL_LEAVE = 'Personal Leave'

WEEKLY_REGULAR_HOURS_LIMIT = 40


class TimePunchCardService(object):

    hash_key_service = HashKeyService()
    request_service = WebRequestService()
    app_feature_service = ApplicationFeatureService()

    def _add_paid_hours_to_week_hours(self, week_hours, hours_number):
        if week_hours.paid_hours >= WEEKLY_REGULAR_HOURS_LIMIT:
            # If for this week, we are already in overtime scenario, just add the hours to overtime
            week_hours.overtime_hours += hours_number
        else:
            # If we are in regular time scenario, add to regular hours
            week_hours.paid_hours += hours_number
            if week_hours.paid_hours > WEEKLY_REGULAR_HOURS_LIMIT:
                # Detect if we just got into overtime scenario
                week_hours.overtime_hours += week_hours.paid_hours - WEEKLY_REGULAR_HOURS_LIMIT
                week_hours.paid_hours = WEEKLY_REGULAR_HOURS_LIMIT

    def _create_weekly_aggregates(self, start_date, end_date):
        # Creates the array of week hours object for
        # every week the start date and end date are part of
        start_week_start_date = start_date - timedelta(days=(start_date.weekday() + 1))
        end_week_end_date = end_date + timedelta(days=(7 - end_date.weekday() - 1))
        weekly_aggregates = []
        week_start_date = start_week_start_date
        while week_start_date < end_week_end_date:
            weekly_aggregates.append({
                'week_start_date': week_start_date,
                'week_end_date': week_start_date + timedelta(days=7),
                'hours': ReportedHours()
            })
            week_start_date += timedelta(days=7)
        return weekly_aggregates

    def get_company_users_time_punch_cards_by_date_range(
        self,
        company_id,
        start_date,
        end_date,
        include_unclosed_cards=False
    ):
        user_punch_cards = []
        api_url = '{0}api/v1/company/{1}/time_punch_cards?start_date={2}&end_date={3}'.format(
            settings.TIME_TRACKING_SERVICE_URL,
            self.hash_key_service.encode_key_with_environment(company_id),
            start_date.isoformat(),
            end_date.isoformat())

        if (include_unclosed_cards):
            api_url = '{0}{1}'.format(api_url, '&includeall=true')

        r = self.request_service.get(api_url)
        if r.status_code == 404:
            return user_punch_cards

        all_entries = r.json()
        for entry in all_entries:
            user_punch_cards.append(TimePunchCard(entry))

        # Sort the cards by user ID
        sorted_cards = sorted(user_punch_cards, key=lambda card: (card.user_id, card.date))

        return sorted_cards

    def get_company_users_daily_time_punch_cards_aggregates(self, company_id, date, include_unclosed_cards=False):
        mappings = {}

        all_cards = self.get_company_users_time_punch_cards_by_date_range(company_id, date, date, include_unclosed_cards)
        for card in all_cards:
            if card.user_id not in mappings:
                mappings[card.user_id] = EmployeeDailyPunchCardAggregate(card.user_id, date)
            mappings[card.user_id].add_card(card)

        unsorted = mappings.values()
        return sorted(unsorted, key=lambda aggregate: aggregate.user_id)

    def get_company_users_reported_hours_by_date_range(
        self,
        company_id,
        start_date,
        end_date,
        include_unclosed_cards=False
    ):
        user_punch_cards = self.get_company_users_time_punch_cards_by_date_range(
                company_id,
                start_date,
                end_date,
                include_unclosed_cards)

        result_dict = {}
        user_weekly_aggregate_dict = {}
        company_feature_list = self.app_feature_service.get_complete_application_feature_status_by_company(company_id)

        for card in user_punch_cards:
            weekly_aggregates = user_weekly_aggregate_dict.get(card.user_id)
            if not weekly_aggregates:
                weekly_aggregates = self._create_weekly_aggregates(start_date, end_date)
                user_weekly_aggregate_dict[card.user_id] = weekly_aggregates

            for week_aggregate in weekly_aggregates:
                # We need to figure our which week does this card belongs to
                if card.date.date() >= week_aggregate['week_start_date'] and card.date.date() < week_aggregate['week_end_date']:
                    # Once we found which week this card belongs to, operate on the week hours object
                    if (card.card_type == PUNCH_CARD_TYPE_PERSONAL_LEAVE):
                        week_aggregate['hours'].unpaid_hours += card.get_punch_card_hours()
                    elif (card.card_type == PUNCH_CARD_TYPE_PAID_TIME_OFF):
                        week_aggregate['hours'].paid_time_off_hours += card.get_punch_card_hours()
                    elif (card.card_type == PUNCH_CARD_TYPE_SICK_TIME):
                        week_aggregate['hours'].sick_time_hours += card.get_punch_card_hours()
                    elif(card.card_type == PUNCH_CARD_TYPE_COMPANY_HOLIDAY):
                        # Holiday hours should be counted as such
                        # except when app feature HolidaysAsWorkingHours is on
                        holiday_default_hours = WEEKLY_REGULAR_HOURS_LIMIT / 5
                        if company_feature_list[APP_FEATURE_HOLIDAYSASWORKINGHOURS]:
                            self._add_paid_hours_to_week_hours(week_aggregate['hours'], holiday_default_hours)

                        week_aggregate['hours'].holiday_hours += holiday_default_hours
                    else:
                        self._add_paid_hours_to_week_hours(week_aggregate['hours'], card.get_punch_card_hours())

        
        for user_id in user_weekly_aggregate_dict:
            # Now sum all weekly hours according their types
            user_hours = ReportedHours()
            weekly_aggregates = user_weekly_aggregate_dict[user_id]
            for week_aggregate in weekly_aggregates:
                user_hours.paid_hours +=week_aggregate['hours'].paid_hours
                user_hours.unpaid_hours += week_aggregate['hours'].unpaid_hours
                user_hours.overtime_hours += week_aggregate['hours'].overtime_hours
                user_hours.paid_time_off_hours += week_aggregate['hours'].paid_time_off_hours
                user_hours.sick_time_hours += week_aggregate['hours'].sick_time_hours
                user_hours.holiday_hours += week_aggregate['hours'].holiday_hours
            
            if company_feature_list[APP_FEATURE_HOLIDAYSASWORKINGHOURS]:
                # If we have this feature on, we should make sure the paid hours are 
                # adjusted without the holiday hours. This is because, on the card
                # aggregate logic above, we double counted already
                user_hours.paid_hours -= user_hours.holiday_hours

            result_dict[user_id] = user_hours
        return result_dict
