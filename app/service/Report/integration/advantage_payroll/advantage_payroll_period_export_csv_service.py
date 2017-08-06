from datetime import date
from dateutil import rrule
import json

from django.contrib.auth import get_user_model

from app.service.Report.integration.payroll_period_export_csv_service_base import (
        PayrollPeriodExportCsvServiceBase,
        EARNING_TYPE_HOURLY,
        EARNING_TYPE_SALARY,
        EARNING_TYPE_OVERTIME,
        EARNING_TYPE_PTO,
        EARNING_TYPE_SICK_TIME
    )
from app.service.integration.integration_provider_service import (
        INTEGRATION_SERVICE_TYPE_PAYROLL,
        INTEGRATION_PAYROLL_ADVANTAGE_PAYROLL
    )

from app.service.compensation_service import (
    PAY_TYPE_HOURLY,
    PAY_TYPE_SALARY
)

User = get_user_model()


class AdvantagePayrollPeriodExportCsvService(PayrollPeriodExportCsvServiceBase):

    def __init__(self):
        super(AdvantagePayrollPeriodExportCsvService, self).__init__()

    #########################################
    ## Override methods - Begin
    #########################################

    def _get_integration_payroll_service_name(self):
        return INTEGRATION_PAYROLL_ADVANTAGE_PAYROLL

    def _needs_write_header_row(self):
        return False

    def _get_pay_code(self, earning_type):
        if (earning_type == EARNING_TYPE_SALARY):
            return 'S'
        elif (earning_type == EARNING_TYPE_HOURLY):
            return 'H'
        elif (earning_type == EARNING_TYPE_PTO):
            return 'PTO'
        elif (earning_type == EARNING_TYPE_SICK_TIME):
            return 'SICK'
        elif (earning_type == EARNING_TYPE_OVERTIME):
            return 'OT'
        else:
            raise ValueError('Unexpected earning type encountered')

    def _write_row(self, row_data):
        self._write_cell(row_data['employee_number'])
        self._write_cell(row_data['full_name'])
        self._write_cell(row_data['pay_type_code'])
        self._write_cell(row_data['pay_rate'])
        self._write_cell(row_data['work_hours'])
        self._write_cell(row_data['division'])
        self._write_cell(row_data['department'])
        self._write_cell(row_data['job'])

        # move to next row
        self._next_row()

    def _get_employee_data_rows(
        self,
        employee_user_id,
        person_info,
        company_info,
        company_payroll_id,
        employee_profile_info,
        employees_reported_hours
    ):
        rows = []

        # If some of the necessary data does not exist, omit the employee
        if (not person_info 
            or not employee_profile_info):
            return rows

        base_row_data = self._get_base_row_data(
            employee_user_id, 
            person_info, 
            company_info,
            company_payroll_id,
            employee_profile_info)

        user_hours = None
        if (employee_user_id in employees_reported_hours):
            user_hours = employees_reported_hours[employee_user_id]

        if (employee_profile_info and employee_profile_info.pay_type == PAY_TYPE_SALARY):
            self._append_earning_type_row(base_row_data, EARNING_TYPE_SALARY, user_hours, rows)
        else:
            self._append_earning_type_row(base_row_data, EARNING_TYPE_HOURLY, user_hours, rows)

        if user_hours:
            if(employee_profile_info and employee_profile_info.pay_type == PAY_TYPE_HOURLY):
                # Write the hours worked over time only for hourly employees
                self._append_earning_type_row(base_row_data, EARNING_TYPE_OVERTIME, user_hours, rows)

            # Write the hours took off for vacations
            self._append_earning_type_row(base_row_data, EARNING_TYPE_PTO, user_hours, rows)

            # Write the hours took off for sick
            self._append_earning_type_row(base_row_data, EARNING_TYPE_SICK_TIME, user_hours, rows)

        return rows

    #########################################
    ## Override methods - End
    #########################################

    def _get_base_row_data(
        self,
        employee_user_id,
        person_info,
        company_info,
        company_payroll_id,
        employee_profile_info):
        row_data = {
            'employee_number': '',
            'full_name': '',
            'pay_type_code': '',
            'pay_rate': '',
            'work_hours': '',
            'division': '',
            'department': '',
            'job': ''
        }

        # First get the employee number that came from AP system
        employee_number = self.integration_provider_service.get_employee_integration_provider_external_id(
            employee_user_id,
            INTEGRATION_SERVICE_TYPE_PAYROLL,
            INTEGRATION_PAYROLL_ADVANTAGE_PAYROLL)

        row_data['employee_number'] = employee_number
        row_data['full_name'] = person_info.get_full_name()

        if (employee_profile_info.department):
            row_data['department'] = employee_profile_info.department.code

        if (employee_profile_info.job):
            row_data['job'] = employee_profile_info.job.code

        if (employee_profile_info.division):
            row_data['division'] = employee_profile_info.division.code

        row_data['pay_rate'] = self._get_employee_pay_rate(employee_profile_info)

        return row_data

    def _append_earning_type_row(self, base_row_data, earning_type, employee_hours, row_list):
        hours = self._get_hours_by_earning_type(earning_type, employee_hours)

        if hours and hours > 0:
            row_data = base_row_data.copy()

            row_data['pay_type_code'] = self._get_pay_code(earning_type)
            row_data['work_hours'] = self._get_hours_by_earning_type(earning_type, employee_hours)

            row_list.append(row_data)

        return

    def _get_employee_pay_rate(self, employee_profile_info):
        if (employee_profile_info.pay_type == PAY_TYPE_HOURLY and employee_profile_info.current_hourly_rate):
            return employee_profile_info.current_hourly_rate
        return ''
