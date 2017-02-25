from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import HttpResponse
from django.http import Http404
from django.db import transaction
from django.db.models import Count, Max
from django.contrib.auth import get_user_model

import xlwt

from app.models.person import Person
from app.models.direct_deposit import DirectDeposit
from app.models.user_bank_account import UserBankAccount

from app.views.permission import (
    user_passes_test,
    company_employer,
    company_employer_or_broker)
from excel_export_view_base import ExcelExportViewBase

User = get_user_model()


class CompanyUsersDirectDepositExcelExportView(ExcelExportViewBase):

    def _write_headers(self, excelSheet, max_direct_deposits):
        col_num = 0
        col_num = self._write_field(excelSheet, 0, col_num, 'First Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Middle Initial')
        col_num = self._write_field(excelSheet, 0, col_num, 'Last Name')

        for i in range(max_direct_deposits):
            col_num = self._write_field(excelSheet, 0, col_num, 'Account Type ' + str(i + 1))
            col_num = self._write_field(excelSheet, 0, col_num, 'Account Issurer ' + str(i + 1))
            col_num = self._write_field(excelSheet, 0, col_num, 'Routing Number ' + str(i + 1))
            col_num = self._write_field(excelSheet, 0, col_num, 'Account Number ' + str(i + 1))
            col_num = self._write_field(excelSheet, 0, col_num, 'Attachment URL ' + str(i + 1))
            col_num = self._write_field(excelSheet, 0, col_num, 'Remainder of Net Pay' + str(i + 1))
            col_num = self._write_field(excelSheet, 0, col_num, 'Amount ' + str(i + 1))
            col_num = self._write_field(excelSheet, 0, col_num, 'Percentage ' + str(i + 1))

        return

    def _write_company(self, company_id, excelSheet):
        user_ids = self._get_all_employee_user_ids_for_company(company_id)

        # for each employee, write direct deposit for him/her
        for i in range(len(user_ids)):
            self._write_employee(user_ids[i], excelSheet, i + 1)

        return

    def _write_employee(self, employee_user_id, excelSheet, row_num):
        start_col_num = 0
        start_col_num = self._write_employee_personal_info(employee_user_id, excelSheet, row_num, start_col_num)
        start_col_num = self._write_employee_direct_deposit(employee_user_id, excelSheet, row_num, start_col_num)
        return

    def _write_employee_personal_info(self, employee_user_id, excelSheet, row_num, start_column_num):
        cur_column_num = start_column_num

        person = None
        persons = Person.objects.filter(user=employee_user_id, relationship='self')
        if (len(persons) > 0):
            person = persons[0]

        # All helpers are built with capability of skiping proper number of columns when
        # person given is None. This is to ensure other information written after these
        # would be written to the right columns
        cur_column_num = self._write_person_basic_info(person, excelSheet, row_num, cur_column_num, employee_user_id)

        return cur_column_num

    def _write_person_basic_info(self, person_model, excelSheet, row_num, col_num, employee_user_id = None):
        if (person_model):
            col_num = self._write_field(excelSheet, row_num, col_num, person_model.first_name)
            col_num = self._write_field(excelSheet, row_num, col_num, person_model.middle_name)
            col_num = self._write_field(excelSheet, row_num, col_num, person_model.last_name)
            return col_num
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
                col_num = self._write_field(excelSheet, row_num, col_num, None)
                col_num = self._write_field(excelSheet, row_num, col_num, user.last_name)

        # Skip the columns
        return col_num + 3

    def _write_employee_direct_deposit(self, employee_user_id, excelSheet, row_num, start_col_num):
        current_col_num = start_col_num

        direct_deposit = None
        direct_deposits = DirectDeposit.objects.filter(user_id=employee_user_id)

        for i in range(len(direct_deposits)):
            current_col_num = self._write_direct_deposit(direct_deposits[i], excelSheet, row_num, current_col_num)

        return current_col_num

    def _write_direct_deposit(self, direct_deposit, excelSheet, row_num, start_col_num):
        current_col_num = start_col_num

        # each direct deposit has only one bank account
        user_bank_account = UserBankAccount.objects.filter(pk=direct_deposit.bank_account.id)[0]

        current_col_num = self._write_field(excelSheet, row_num, current_col_num, user_bank_account.account_type)
        current_col_num = self._write_field(excelSheet, row_num, current_col_num, user_bank_account.bank_name)
        current_col_num = self._write_field(excelSheet, row_num, current_col_num, user_bank_account.routing)
        current_col_num = self._write_field(excelSheet, row_num, current_col_num, user_bank_account.account)
        current_col_num = self._write_field(excelSheet, row_num, current_col_num, user_bank_account.attachment)

        is_ronp = 'Yes' if direct_deposit.remainder_of_all else 'No'

        current_col_num = self._write_field(excelSheet, row_num, current_col_num, is_ronp)
        current_col_num = self._write_field(excelSheet, row_num, current_col_num, direct_deposit.amount)
        current_col_num = self._write_field(excelSheet, row_num, current_col_num, direct_deposit.percentage)

        return current_col_num

    ''' Direct Deposit summary is expected to be visible to employer only
        Broker should not need such information
    '''
    @user_passes_test(company_employer)
    def get(self, request, pk, format=None):
        book = xlwt.Workbook(encoding='utf8')
        sheet = book.add_sheet('Direct Deposit')

        # Pre compute the max number of dependents across all employees of
        # the company, so we know how many sets of headers for dependent
        # info we need to populate
        max_direct_deposits = self._get_max_direct_deposit_count(pk)
        self._write_headers(sheet, max_direct_deposits)

        self._write_company(pk, sheet)

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=employee_direct_deposit.xls'
        book.save(response)
        return response
