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
        INTEGRATION_PAYROLL_CONNECT_PAYROLL
    )

from app.service.compensation_service import (
    PAY_TYPE_HOURLY,
    PAY_TYPE_SALARY
)

User = get_user_model()


class ConnectPayrollPeriodExportCsvService(PayrollPeriodExportCsvServiceBase):

    def __init__(self):
        super(ConnectPayrollPeriodExportCsvService, self).__init__()

    #########################################
    ## Override methods - Begin
    #########################################

    def _get_integration_payroll_service_name(self):
        return INTEGRATION_PAYROLL_CONNECT_PAYROLL

    def _needs_write_header_row(self):
        return True

    def _write_headers(self):
        self._write_cell('File Type')
        self._write_cell('Client Name')
        self._write_cell('Client Number')
        self._write_cell('Employee Number')
        self._write_cell('Employee Name')
        self._write_cell('SSN')
        self._write_cell('Earning Name')
        self._write_cell('Earning Code')
        self._write_cell('Hours')
        self._write_cell('Pay Rate')
        self._write_cell('Fixed $ Amount')
        self._write_cell('Location')
        self._write_cell('Division')
        self._write_cell('Department')
        self._write_cell('Job Code')
        self._write_cell('Beginning Balance')
        self._write_cell('Accrued')
        self._write_cell('Used')
        self._write_cell('Ending Balance')

        self._next_row()

    def _get_pay_code(self, earning_type):
        # TODO: 
        #    Confirm the list of pay codes 
        #    Confirm expectation of salary based employees
        if (earning_type == EARNING_TYPE_SALARY):
            return 'REG'
        elif (earning_type == EARNING_TYPE_HOURLY):
            return 'REG'
        elif (earning_type == EARNING_TYPE_PTO):
            return 'VAC'
        elif (earning_type == EARNING_TYPE_SICK_TIME):
            return 'SICK'
        elif (earning_type == EARNING_TYPE_OVERTIME):
            return 'OT'
        else:
            raise ValueError('Unexpected earning type encountered')

    def _get_pay_name(self, earning_type):
        # TODO:
        #    Confirm the list of pay type names
        #    Confirm expectation of salary based employees
        if (earning_type == EARNING_TYPE_SALARY):
            return 'Regular'
        elif (earning_type == EARNING_TYPE_HOURLY):
            return 'Regular'
        elif (earning_type == EARNING_TYPE_PTO):
            return 'Vacation'
        elif (earning_type == EARNING_TYPE_SICK_TIME):
            return 'Sick'
        elif (earning_type == EARNING_TYPE_OVERTIME):
            return 'Overtime'
        else:
            raise ValueError('Unexpected earning type encountered')

    def _write_row(self, row_data):
        self._write_cell(row_data['file_type'])
        self._write_cell(row_data['client_name'])
        self._write_cell(row_data['client_number'])
        self._write_cell(row_data['employee_number'])
        self._write_cell(row_data['employee_name'])
        self._write_cell(row_data['ssn'])
        self._write_cell(row_data['earning_name'])
        self._write_cell(row_data['earning_code'])
        self._write_cell(row_data['hours'])
        self._write_cell(row_data['pay_rate'])
        self._write_cell(row_data['amount'])
        self._write_cell(row_data['location'])
        self._write_cell(row_data['division'])
        self._write_cell(row_data['department'])
        self._write_cell(row_data['job_code'])
        self._write_cell(row_data['pto_beginning_balance'])
        self._write_cell(row_data['pto_accrued'])
        self._write_cell(row_data['pto_used'])
        self._write_cell(row_data['pto_ending_balance'])

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

        employee_pay_type = self._get_employee_pay_type(company_info, employee_user_id, employee_profile_info)
        if (employee_pay_type == PAY_TYPE_SALARY):
            self._append_earning_type_row(base_row_data, EARNING_TYPE_SALARY, user_hours, rows)
        else:
            self._append_earning_type_row(base_row_data, EARNING_TYPE_HOURLY, user_hours, rows)

        if user_hours:
            if(employee_pay_type == PAY_TYPE_HOURLY):
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
            'file_type': 'Agile',
            'client_name': '',
            'client_number': '',
            'employee_number': '',
            'employee_name': '',
            'ssn': '',
            'earning_name': '',
            'earning_code': '',
            'hours': '',
            'pay_rate': '',
            'amount': '',
            'location': '',
            'division': '',
            'department': '',
            'job_code': '',
            'pto_beginning_balance': '',
            'pto_accrued': '',
            'pto_used': '',
            'pto_ending_balance': ''
        }

        row_data['client_name'] = company_info.company_name
        row_data['client_number'] = company_payroll_id

        row_data['employee_number'] = employee_profile_info.employee_number
        row_data['employee_name'] = person_info.get_full_name()

        if (employee_profile_info.department):
            row_data['department'] = employee_profile_info.department.code

        if (employee_profile_info.job):
            row_data['job_code'] = employee_profile_info.job.code

        # TODO: Confirm
        # According to Doc, Location and Division is currently not supported
        # Also the sample file does not even have Division listed as a column

        return row_data

    def _append_earning_type_row(self, base_row_data, earning_type, employee_hours, row_list):
        hours = self._get_hours_by_earning_type(earning_type, employee_hours)

        if hours and hours > 0:
            row_data = base_row_data.copy()

            row_data['earning_name'] = self._get_pay_name(earning_type)
            row_data['earning_code'] = self._get_pay_code(earning_type)
            row_data['hours'] = self._get_hours_by_earning_type(earning_type, employee_hours)

            row_list.append(row_data)

        return

    def _get_employee_pay_type(self, company_info, employee_user_id, employee_profile_info):
        if not employee_profile_info:
            return None
        time_tracking_setting = self.time_punch_card_service.get_time_tracking_setting_for_user(
            company_info.company_id,
            employee_user_id
        )

        if time_tracking_setting and time_tracking_setting['autoReportFullWeek']['active']:
            return PAY_TYPE_SALARY
        else:
            return employee_profile_info.pay_type
