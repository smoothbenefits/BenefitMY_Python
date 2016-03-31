import xlwt
from datetime import datetime
from rest_framework.response import Response
from django.http import HttpResponse, Http404
from django.contrib.auth import get_user_model
from app.models.person import Person
from app.models.company import Company
from app.models.employee_profile import EmployeeProfile, FULL_TIME
from app.service.compensation_service import CompensationService

from app.views.permission import (
    user_passes_test,
    company_employer,
    company_employer_or_broker)
from excel_export_view_base import ExcelExportViewBase
from app.service.time_tracking_service import TimeTrackingService

FULL_TIME_DEFAULT_WEEKLY_HOURS = 40
User = get_user_model()

class CompanyUsersWorktimeWeeklyReportView(ExcelExportViewBase):

    def _write_headers(self, excelSheet):
        col_num = 0
        col_num = self._write_field(excelSheet, 0, col_num, 'Company')
        col_num = self._write_field(excelSheet, 0, col_num, 'Week Start Date')
        col_num = self._write_field(excelSheet, 0, col_num, 'First Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Last Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'State')
        col_num = self._write_field(excelSheet, 0, col_num, 'Payroll Frequency')
        col_num = self._write_field(excelSheet, 0, col_num, 'Regular Hours')
        col_num = self._write_field(excelSheet, 0, col_num, 'Regular Gross Pay')
        col_num = self._write_field(excelSheet, 0, col_num, 'OT Hours')

        return


    def _get_company_info(self, company_id):
        try:
            return Company.objects.get(pk=company_id)
        except Company.DoesNotExist:
            raise Http404

    def _get_user_timesheet(self, user_id, timesheets):
        try:
            return next(x for x in timesheets if x['user_id'] == user_id)
        except StopIteration:
            return None

    def _get_employee_person_and_profile(self, employee_user_id, company):
        person = None
        profile = None
        persons = Person.objects.filter(user=employee_user_id, relationship='self')
        if (len(persons) > 0):
            person = persons[0]
        
        if person:
            profile = EmployeeProfile.objects.filter(person=person, company=company)
            if len(profile) > 0:
                profile = profile[0]

        return person, profile

    def _write_company(self, company, week_start_date, excelSheet, submitted_sheets):
        users_id = self._get_all_employee_user_ids_for_company(company.id)
        row_num = 1
        # For each of them, write out his/her information
        for i in range(len(users_id)):
            user_id = users_id[i]
            row_num = self._write_employee(company, week_start_date, user_id, excelSheet, row_num, self._get_user_timesheet(user_id, submitted_sheets))

        return

    def _write_employee(self, company, week_start_date, employee_user_id, excelSheet, row_num, user_time_sheet):
        if not user_time_sheet:
            row_num = self._write_employee_row(company, week_start_date, employee_user_id, None, excelSheet, row_num)
        else:
            for timecard in user_time_sheet['timecards']:
                row_num = self._write_employee_row(company, week_start_date, employee_user_id, timecard, excelSheet, row_num)
        return row_num

    def _write_employee_row(self, company, week_start_date, employee_user_id, timecard, excelSheet, row_num):
        col_num = 0
        person, profile = self._get_employee_person_and_profile(employee_user_id, company)
        col_num = self._write_field(excelSheet, row_num, col_num, company.name)
        col_num = self._write_field(excelSheet, row_num, col_num, week_start_date.strftime('%m/%d/%Y'))
        col_num = self._write_person_name_info(person, excelSheet, row_num, col_num, employee_user_id)
        col_num = self._write_state_info(timecard, excelSheet, row_num, col_num)
        col_num = self._write_field(excelSheet, row_num, col_num, company.pay_period_definition.name if company.pay_period_definition else '')
        col_num = self._write_week_total(timecard, profile, excelSheet, row_num, col_num)
        col_num = self._write_regular_pay(timecard, person, profile, excelSheet, row_num, col_num)
        col_num = self._write_overtime_hours(timecard, excelSheet, row_num, col_num)
        return row_num + 1 

    def _write_person_name_info(self, person_model, excelSheet, row_num, col_num, employee_user_id = None):
        if (person_model):
            col_num = self._write_field(excelSheet, row_num, col_num, person_model.first_name)
            col_num = self._write_field(excelSheet, row_num, col_num, person_model.last_name)
        elif (employee_user_id):
            # TODO:
            # This is not a clean solution, but is the only one we have for the short term
            # The desire is to also include some basic information for an employee, even if
            # he has not gone through on-boarding yet
            # So without the person profile that is filled out during onboarding, all we can
            # do for now is to grab the basic information from the user account.
            users = User.objects.filter(pk=employee_user_id)
            if (len(users) > 0):
                user = users[0]
                col_num = self._write_field(excelSheet, row_num, col_num, user.first_name)
                col_num = self._write_field(excelSheet, row_num, col_num, user.last_name)
            else:
                col_num += 2
        else:
            # Skip the columns
            col_num += 2

        return col_num

    def _write_state_info(self, timecard, excelSheet, row_num, col_num):
        if timecard and timecard.get('tags') and 'State' in timecard['tags'][0]['tagType']:    
            col_num = self._write_field(excelSheet, row_num, col_num, timecard['tags'][0]['tagContent'])
            return col_num
        else:
            return col_num + 1

    def _write_week_total(self, timecard, profile, excelSheet, row_num, col_num):
        if not timecard:
            default = FULL_TIME_DEFAULT_WEEKLY_HOURS if profile and profile.employment_type == FULL_TIME else 0
            col_num = self._write_field(excelSheet, row_num, col_num, default)
        else:
            week_total_hours = self._get_week_total(timecard, 'workHours')
            if week_total_hours:
                col_num = self._write_field(excelSheet, row_num, col_num, week_total_hours)
            else:
                col_num += 1
        
        return col_num

    def _write_regular_pay(self, timecard, person, profile, excelSheet, row_num, col_num):
        weekly_pay = None
        if person:
            compensation_service = CompensationService(person.id, profile)
            week_total_hours = 0
            if timecard:
                week_total_hours = self._get_week_total(timecard, 'workHours')
            weekly_pay = compensation_service.get_current_weekly_salary(week_total_hours)

        if weekly_pay:
            col_num = self._write_field(excelSheet, row_num, col_num, '{0:.2f}'.format(weekly_pay))
        else:
            col_num = self._write_field(excelSheet, row_num, col_num, 'Salary Not Available')

        return col_num

    def _write_overtime_hours(self, timecard, excelSheet, row_num, col_num):
        if not timecard:
            col_num += 1
        else:
            week_total_hours = self._get_week_total(timecard, 'overtimeHours')
            if week_total_hours:
                col_num = self._write_field(excelSheet, row_num, col_num, week_total_hours)
            else:
                col_num += 1
        
        return col_num

    def _get_week_total(self, timecard, field):
        work_hours = timecard.get(field)
        total = None
        if work_hours:
            total = 0
            for day in work_hours.values():
                total += day['hours']
        return int(total)

    ''' Employer should be able to get work time summary 
        report of the employees within the company
    '''
    @user_passes_test(company_employer)
    def get(self, request, pk, year, month, day, format=None):
        comp = self._get_company_info(pk)
        week_start_date = datetime(year=int(year), month=int(month), day=int(day))
        book = xlwt.Workbook(encoding='utf8')
        sheet = book.add_sheet('Timesheet')
        time_tracking_service = TimeTrackingService()
        submitted_sheets = time_tracking_service.get_company_users_submitted_work_timesheet_by_week_start_date(
            comp.id,
            week_start_date)

        self._write_headers(sheet)

        self._write_company(comp, week_start_date, sheet, submitted_sheets)

        response = HttpResponse(content_type='application/vnd.ms-excel')
        # Need company name:

        response['Content-Disposition'] = (
            'attachment; filename={0}_employee_worktime_report_{1}.xls'
        ).format(comp, week_start_date.strftime('%m_%d_%Y'))
        book.save(response)
        return response
