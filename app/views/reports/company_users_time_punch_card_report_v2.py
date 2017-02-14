from datetime import (date, timedelta)
from collections import OrderedDict
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from copy import deepcopy

from app.views.permission import (
    user_passes_test,
    company_employer)
from excel_export_view_base import ExcelExportViewBase
from app.service.date_time_service import DateTimeService
from app.service.time_punch_card_service import (
    TimePunchCardService,
    PUNCH_CARD_TYPE_WORK_TIME,
    PUNCH_CARD_TYPE_COMPANY_HOLIDAY,
    PUNCH_CARD_TYPE_PAID_TIME_OFF,
    PUNCH_CARD_TYPE_SICK_TIME,
    PUNCH_CARD_TYPE_PERSONAL_LEAVE)
from app.service.company_personnel_service import CompanyPersonnelService


# In the following dictionary,
# "NoHours": used to determine whether we should
#     assign 8 hours to the days where this record type exists.
# "PrePopulate": used to determine whether we should pre-populate the default
#     set of hours for each employee even if there are no such record of the type exists

CARD_TYPES = OrderedDict([
    (PUNCH_CARD_TYPE_WORK_TIME, {'name': 'Worked Hours', 'NoHours': False, 'PrePopulate': True}),
    (PUNCH_CARD_TYPE_SICK_TIME, {'name': 'Sick Time', 'NoHours': False, 'PrePopulate': True}),
    (PUNCH_CARD_TYPE_PAID_TIME_OFF, {'name': 'PTO', 'NoHours': False, 'PrePopulate': True}),
    (PUNCH_CARD_TYPE_COMPANY_HOLIDAY, {'name': 'Company Holiday', 'NoHours': True, 'PrePopulate': True}),
    (PUNCH_CARD_TYPE_PERSONAL_LEAVE, {'name': 'Personal Leave (unpaid)', 'NoHours': False, 'PrePopulate': False})
])

DATE_FORMAT_STRING = '%m/%d/%Y'

# For the case where a card type does not expect user
# specified hours (such as Company Holiday), use the
# below default
TIME_PUNCH_CARD_NO_HOURS_DEFAULT_HOURS = 8

# Placeholder state string to use when user not specified
TIME_PUNCH_CARD_NON_SPECIFIED_STATE = 'State Not Specified'

User = get_user_model()


class CompanyUsersTimePunchCardWeeklyReportV2View(ExcelExportViewBase):

    date_time_service = DateTimeService()
    time_punch_card_service = TimePunchCardService()
    company_personnel_service = CompanyPersonnelService()

    def __init__(self):
        # List out instance variables that will be used
        # below
        self._company = None
        self._week_start_date = None
        self._week_end_date = None
        self._employee_list_cache = None
        self._blank_state_sheet_data_template = None

    def _build_employee_info_cache(self):
        self._employee_list_cache = []
        all_employees = self._get_all_employee_users_for_company(self._company.id)
        filtered_employee_user_ids = self.company_personnel_service.get_company_employee_user_ids_non_fully_terminated_in_time_range(
            self._company.id,
            self._week_start_date,
            self._week_end_date
        )
        for employee in all_employees:
            if (employee.id in filtered_employee_user_ids):
                self._employee_list_cache.append({
                    'user_id': employee.id,
                    'full_name': self._get_user_full_name(employee)
                })

    def _build_report_time_sheets_data(self):
        # The structure of the result would be a nested dictionary
        # result{ state: { card_type: { user_id: { weekday_index: hours } } } }
        all_state_sheets = {}

        # First read in all employee submitted cards
        all_cards = self._get_all_punch_cards()

        # Now setup blank/base sheet data for all states
        # encountered
        if (len(all_cards) <= 0):
            state = 'No State'
            all_state_sheets.setdefault(
                        state,
                        self._get_blank_sheet_data())
        else:
            for card in all_cards:
                state = card.state
                if (not state):
                    state = TIME_PUNCH_CARD_NON_SPECIFIED_STATE
                if (state not in all_state_sheets):
                    all_state_sheets.setdefault(
                        state,
                        self._get_blank_sheet_data())

        # Now "merge" user submitted data into the sheets
        # data
        for punch_card in all_cards:
            self._merge_punch_card_data_to_full_set(
                punch_card,
                all_state_sheets)

        return all_state_sheets

    def _get_all_punch_cards(self):
        return self.time_punch_card_service.get_company_users_time_punch_cards_by_date_range(
            self._company.id,
            self._week_start_date,
            self._week_end_date)

    def _get_blank_sheet_data(self):
        # Cache a copy as template and return deep copies of that
        # to save some computational power
        if (not self._blank_state_sheet_data_template):
            sheet_data = {}
            for card_type in CARD_TYPES:
                sheet_data.setdefault(
                    card_type,
                    self._get_blank_card_type_section_data(card_type))
            self._blank_state_sheet_data_template = sheet_data

        return deepcopy(self._blank_state_sheet_data_template)

    def _get_blank_card_type_section_data(self, card_type):
        card_type_section_data = {}

        card_type_behavior = CARD_TYPES[card_type]

        if card_type_behavior.get('PrePopulate', True):
            for user_info in self._employee_list_cache:
                card_type_section_data.setdefault(
                    user_info['user_id'],
                    self._get_employee_weekly_blank_data())

        return card_type_section_data

    def _get_employee_weekly_blank_data(self):
        blank_data = {}
        for isoweekday in range(7):
            blank_data.setdefault(isoweekday, 0.0)
        return blank_data

    def _merge_punch_card_data_to_full_set(self, punch_card, all_states_sheets_data):
        state_data = all_states_sheets_data[punch_card.state]
        card_type = punch_card.card_type
        if (card_type in CARD_TYPES):
            card_type_data = state_data[card_type]
            if punch_card.user_id not in card_type_data:
                card_type_data.setdefault(
                    punch_card.user_id,
                    self._get_employee_weekly_blank_data())
            employee_weekly_data = card_type_data[punch_card.user_id]
            card_weekday_iso = punch_card.get_card_day_of_week_iso()
            if (CARD_TYPES[card_type].get('NoHours', True)):
                # Even if an employee filed 2 of such cards in one slot
                # Only count hours once
                if (employee_weekly_data[card_weekday_iso] <= 0):
                    employee_weekly_data[card_weekday_iso] = TIME_PUNCH_CARD_NO_HOURS_DEFAULT_HOURS
            else:
                # Accumulate the hours specified by the card
                hours = punch_card.get_punch_card_hours()   
                employee_weekly_data[card_weekday_iso] += hours

    def _write_all_states_sheets(self, all_states_sheets_data):
        for state in all_states_sheets_data:
            self._write_state_sheet(state, all_states_sheets_data[state])

    def _write_state_sheet(self, state, state_sheet_data):
        self._start_work_sheet(state)
        self._write_sheet_headers(state)

        for card_type in CARD_TYPES:
            self._write_card_type_section(card_type, state_sheet_data[card_type])

    def _write_sheet_headers(self, state):
        self._write_cell('Company')
        self._write_cell(self._company.name)
        self._next_row()
        self._write_cell('Payroll Sheet')
        self._write_cell(self._week_start_date.strftime(DATE_FORMAT_STRING))
        self._write_cell(self._week_end_date.strftime(DATE_FORMAT_STRING))
        self._next_row()
        self._write_cell('State')
        self._write_cell(state)
        self._next_row()
        self._next_row()

    def _write_card_type_section(self, card_type, card_type_section_data):
        card_type_behavior = CARD_TYPES[card_type]
        self._write_cell(card_type_behavior['name'])
        self._next_row()
        self._write_card_type_section_headers()

        # Now write the data
        for user_info in self._employee_list_cache:
            user_id = user_info['user_id']
            if (user_id in card_type_section_data):
                self._write_employee_weekly_data(
                    user_info,
                    card_type_section_data[user_id])

        self._next_row()

    def _write_card_type_section_headers(self):
        self._write_cell('Employee Name')
        for i in range(7):
            date = self._week_start_date + timedelta(i)
            header_text = '{} - {}'.format(date.strftime('%A'), date.strftime(DATE_FORMAT_STRING))
            self._write_cell(header_text) 
        self._next_row()

    def _write_employee_weekly_data(self, user_info, employee_weekly_data):
        self._write_cell(user_info['full_name'])
        for weekdayiso in range(7):
            self._write_cell(employee_weekly_data[weekdayiso])
        self._next_row()

    '''
    Get the Weekly Time Punch Card report excel of a company's all employees
    '''
    @user_passes_test(company_employer)
    def get(self, request, pk, year, month, day, format=None):
        # Parse all information needed from URL
        self._company = self._get_company_info(pk)
        input_date = date(year=int(year), month=int(month), day=int(day))
        week_range = self.date_time_service.get_week_range_by_date(input_date)
        self._week_start_date = week_range[0]
        self._week_end_date = week_range[1]

        # First collect and cache company employees data
        self._build_employee_info_cache()

        # Now collect time punch data for the given week
        # and organize them to the right hierarchy
        all_states_sheets_data = self._build_report_time_sheets_data()

        # Now write out all data
        self._init()
        self._write_all_states_sheets(all_states_sheets_data)

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = (
            'attachment; filename={0}_employee_worktime_report_{1}.xls'
        ).format(self._company, self._week_start_date.strftime('%m_%d_%Y'))

        self._save(response)

        return response
