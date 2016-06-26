from datetime import datetime, timedelta
from datetime import date
import json
from rest_framework.response import Response
from django.http import HttpResponse, Http404
from django.contrib.auth import get_user_model
from app.models.person import Person
from app.models.company import Company
from app.models.employee_profile import EmployeeProfile, FULL_TIME
from app.models.workers_comp.employee_phraseology import EmployeePhraseology
from app.service.compensation_service import CompensationService

from app.views.permission import (
    user_passes_test,
    company_employer,
    company_employer_or_broker)
from excel_export_view_base import ExcelExportViewBase
from app.service.time_tracking_service import TimeTrackingService
from app.service.date_time_service import DateTimeService

FULL_TIME_DEFAULT_WEEKLY_HOURS = 40

RECORD_TYPES = [
    'Work Day',
    'Company Holiday',
    'Paid Time Off',
    'Sick Time',
    'Personal Leave'
]

WEEK_DAYS = [
    'sunday',
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'saturday'
]

User = get_user_model()


class CompanyUsersTimePunchCardWeeklyReportView(ExcelExportViewBase):

    user_id_name_cache = {}

    def _empty_employee_entry(self):
        record_entry = {}
        for week_day_key in WEEK_DAYS:
            record_entry[week_day_key] = {
                'hours': 0,
                'timeRange': {
                    'start': None,
                    'end': None
                }
            }
        return record_entry

    def _set_record_type_mapped_report_entry(
        self,
        record_type,
        entries_by_record_type,
        time_card,
        user_id):

        for week_day in time_card['workHours']:
            week_day_record = time_card['workHours'][week_day]
            if week_day_record['recordType'] == record_type:
                record_type_entry = entries_by_record_type.setdefault(record_type, {})
                employee_entry = record_type_entry.setdefault(
                    user_id,
                    self._empty_employee_entry())
                employee_entry[week_day]['hours'] = week_day_record['hours']
                employee_entry[week_day]['timeRange'] = week_day_record['timeRange']


    def _set_record_type_sorted_report_entries(self, time_card, entries_by_record_type, user_id):
        for record_type in RECORD_TYPES:
            self._set_record_type_mapped_report_entry(
                record_type,
                entries_by_record_type,
                time_card,
                user_id)
        return entries_by_record_type

    def _new_entries_by_record_type(self):
        entries_by_record_type = {}
        for record_type in RECORD_TYPES:
            entries_by_record_type[record_type] = {}
        return entries_by_record_type

    def _build_user_id_name_cache(self, user_id, company):
        if not self.user_id_name_cache.get(user_id):
            person = None
            profile = None
            persons = Person.objects.filter(user=user_id, relationship='self')
            if (len(persons) > 0):
                person = persons[0]

            if person:
                profile = EmployeeProfile.objects.filter(person=person, company=company)
                if len(profile) > 0:
                    profile = profile[0]

            self.user_id_name_cache[user_id] = {
                'person': person,
                'profile': profile
            }

    def _get_report_entries_by_state_and_type(self, timesheet_by_employee, company):
        report_entries_by_state = {}
        for employee_time_sheet in timesheet_by_employee:
            for employee_time_card in employee_time_sheet['timecards']:
                state_key = 'State Not Specified'
                state_tag = next(
                    (x for x in employee_time_card['tags'] if x['tagType'] == 'ByState'),
                    None
                )
                
                if state_tag:
                    state_key = state_tag['tagContent']

                entries_by_record_type = report_entries_by_state.get(
                    state_key,
                    {})
                
                self._set_record_type_sorted_report_entries(
                    employee_time_card, 
                    entries_by_record_type,
                    employee_time_sheet['user_id'])

                self._build_user_id_name_cache(employee_time_sheet['user_id'], company)

                report_entries_by_state[state_key] = entries_by_record_type

        return report_entries_by_state

    def _get_company_info(self, company_id):
        try:
            return Company.objects.get(pk=company_id)
        except Company.DoesNotExist:
            raise Http404

    def _write_record_type_entry_headers(self, excel_sheet, row):
        self._write_field(excel_sheet, row, 0, 'Employee Name')
        self._write_field(excel_sheet, row, 1, 'Monday - Date')
        self._write_field(excel_sheet, row, 2, 'Tuesday - Date')
        self._write_field(excel_sheet, row, 3, 'Wednesday - Date')
        self._write_field(excel_sheet, row, 4, 'Thursday - Date')
        self._write_field(excel_sheet, row, 5, 'Friday - Date')
        self._write_field(excel_sheet, row, 6, 'Saturday - Date')
        self._write_field(excel_sheet, row, 7, 'Sunday - Date')
        return row + 1


    def _write_record_type_entry(self, excel_sheet, record_type_entry, row):
        row = self._write_record_type_entry_headers(excel_sheet, row)
        for user_id in record_type_entry:
            user_info = self.user_id_name_cache.get(user_id)
            self._write_field(excel_sheet, row, 0, '{} {}'.format(
                user_info['person'].first_name,
                user_info['person'].last_name)
            )
            self._write_field(excel_sheet, row, 1, record_type_entry.get(user_id)['monday']['hours'])
            self._write_field(excel_sheet, row, 2, record_type_entry.get(user_id)['tuesday']['hours'])
            self._write_field(excel_sheet, row, 3, record_type_entry.get(user_id)['wednesday']['hours'])
            self._write_field(excel_sheet, row, 4, record_type_entry.get(user_id)['thursday']['hours'])
            self._write_field(excel_sheet, row, 5, record_type_entry.get(user_id)['friday']['hours'])
            self._write_field(excel_sheet, row, 6, record_type_entry.get(user_id)['saturday']['hours'])
            self._write_field(excel_sheet, row, 7, record_type_entry.get(user_id)['sunday']['hours'])
            row += 1
        return row + 2
        

    def _write_state_time_cards(self, excel_sheet, state_entry):
        row = 4
        col = 0
        for record_type in state_entry:
            self._write_field(excel_sheet, row, col, record_type)
            row += 1
            row = self._write_record_type_entry(excel_sheet, state_entry[record_type], row)

    '''
    Get the Weekly Time Punch Card report excel of a company's all employees
    '''
    @user_passes_test(company_employer)
    def get(self, request, pk, year, month, day, format=None):
        comp = self._get_company_info(pk)
        week_start_date = date(year=int(year), month=int(month), day=int(day))
        week_end_date = week_start_date + timedelta(7)
        self._init()
        
        time_tracking_service = TimeTrackingService()
        submitted_sheets_by_employee = time_tracking_service.get_company_users_submitted_work_timesheet_by_week_range(
            comp.id,
            week_start_date,
            week_end_date)

        report_entries_by_state = self._get_report_entries_by_state_and_type(
            submitted_sheets_by_employee.get(week_start_date, []),
            comp
        )

        #response = HttpResponse(json.dumps(report_entries_by_state), content_type='application/json')
        #return response

        for state_key in report_entries_by_state:
            self._start_work_sheet(state_key)
            self._write_state_time_cards(self._current_work_sheet, report_entries_by_state[state_key])


        response = HttpResponse(content_type='application/vnd.ms-excel')

        # Need company name:
        
        response['Content-Disposition'] = (
            'attachment; filename={0}_employee_worktime_report_{1}.xls'
        ).format(comp, week_start_date.strftime('%m_%d_%Y'))
        self._save(response)
        return response
