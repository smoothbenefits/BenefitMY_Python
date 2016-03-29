import xlwt
from datetime import datetime
from rest_framework.response import Response
from django.http import HttpResponse, Http404
from django.contrib.auth import get_user_model
from app.models.person import Person
from app.models.company import Company

from app.views.permission import (
    user_passes_test,
    company_employer,
    company_employer_or_broker)
from excel_export_view_base import ExcelExportViewBase

User = get_user_model()

class CompanyUsersWorktimeWeeklyReportView(ExcelExportViewBase):

    _week_start_date = None

    def _write_headers(self, excelSheet):
        col_num = 0
        col_num = self._write_field(excelSheet, 0, col_num, 'Company')
        col_num = self._write_field(excelSheet, 0, col_num, 'Dates')
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


    def _write_company(self, company, excelSheet):
        users_id = self._get_all_employee_user_ids_for_company(company.id)

        # For each of them, write out his/her information
        for i in range(len(users_id)):
            self._write_employee(company, users_id[i], excelSheet, i + 1)

        return

    def _write_employee(self, company, employee_user_id, excelSheet, row_num):
        start_column_num = 0
        start_column_num = self._write_employee_personal_info(company, employee_user_id, excelSheet, row_num, start_column_num)

        # Now let's get this employee's timesheet info
        return

    def _write_employee_personal_info(self, company, employee_user_id, excelSheet, row_num, start_column_num):
        cur_column_num = start_column_num

        cur_column_num = self._write_field(excelSheet, row_num, cur_column_num, company.name)
        # The dates column are intentionally left blank for now
        cur_column_num += 1

        person = None
        persons = Person.objects.filter(user=employee_user_id, relationship='self')
        if (len(persons) > 0):
            person = persons[0]

        # All helpers are built with capability of skiping proper number of columns when
        # person given is None. This is to ensure other information written after these
        # would be written to the right columns
        cur_column_num = self._write_person_name_info(person, excelSheet, row_num, cur_column_num, employee_user_id)

        return cur_column_num


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
            # Skip the columns
            col_num = col_num + 3

        return col_num


    ''' Employer should be able to get work time summary 
        report of the employees within the company
    '''
    @user_passes_test(company_employer)
    def get(self, request, pk, year, month, day, format=None):
        comp = self._get_company_info(pk)
        self._week_start_date = datetime(year=int(year), month=int(month), day=int(day))
        book = xlwt.Workbook(encoding='utf8')
        sheet = book.add_sheet('Timesheet')
        self._write_headers(sheet)

        self._write_company(comp, sheet)

        response = HttpResponse(content_type='application/vnd.ms-excel')
        # Need company name:

        response['Content-Disposition'] = (
            'attachment; filename={0}_employee_worktime_report_{1}.xls'
        ).format(comp, self._week_start_date)
        book.save(response)
        return response