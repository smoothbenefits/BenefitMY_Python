from datetime import date
from dateutil import rrule
import json

from django.contrib.auth import get_user_model

from app.models.employee_profile import (
    EMPLOYMENT_STATUS_ACTIVE,
    EMPLOYMENT_STATUS_TERMINATED
)
from app.service.compensation_service import (
    PAY_TYPE_HOURLY,
    PAY_TYPE_SALARY
)

from app.factory.report_view_model_factory import ReportViewModelFactory

from app.service.time_punch_card_service import TimePunchCardService
from app.service.integration.integration_provider_service import (
        IntegrationProviderService,
        INTEGRATION_SERVICE_TYPE_PAYROLL,
        INTEGRATION_PAYROLL_CONNECT_PAYROLL
    )
from app.service.Report.csv_report_service_base import CsvReportServiceBase

User = get_user_model()
OVERTIME_PAY_CODE = 'OT'
PAID_TIME_OFF_CODE = 'PTO'
SICK_TIME_CODE = 'SICK'
SALARY_EMPLOYEE_HOURS_PER_DAY = 8


class ConnectPayrollPeriodExportCsvService(CsvReportServiceBase):
    
    ''' Big assumptions and TODOs
        * The expectation for this export is weekly
        * Though salary rate exported here is per pay period
        * Personal Leave is the only card type that does not count towards hours reported
        * Company Holiday is counted as 8 hours
        * Only export employee's who is at least partially active in the period
        * The report does not try to prorate if employee was terminated during the period. 
    '''

    def __init__(self):
        super(ConnectPayrollPeriodExportCsvService, self).__init__()
        self.view_model_factory = ReportViewModelFactory()
        self.time_punch_card_service = TimePunchCardService()
        self.integration_provider_service = IntegrationProviderService()
        self.week_days = 0

    def get_report(self, company_id, period_start, period_end, outputStream):
        ap_client_id = self._get_ap_client_number(company_id)
        if (not ap_client_id):
            raise ValueError('The company is not properly configured to integrate with Connect Payroll service!')
        self.week_days = self._get_week_day_number(period_start, period_end)
        self._write_company(company_id, period_start, period_end)
        self._save(outputStream)

    def _get_ap_client_number(self, company_id):
        return self.integration_provider_service.get_company_integration_provider_external_id(
            company_id,
            INTEGRATION_SERVICE_TYPE_PAYROLL,
            INTEGRATION_PAYROLL_CONNECT_PAYROLL)

    def _write_company(self, company_id, period_start, period_end):
        user_ids = self._get_all_employee_user_ids_for_company(company_id)

        # Get the time tracking data for the company, for the date period
        # specified
        employees_reported_hours = self.time_punch_card_service.get_company_users_reported_hours_by_date_range(
            company_id, period_start, period_end)

        # For each of them, write out his/her information
        for i in range(len(user_ids)):
            employee_user_id = user_ids[i]
            employee_profile_info = self.view_model_factory.get_employee_employment_profile_data(
                                    employee_user_id,
                                    company_id)

            # Only report if the employee was, at least partially, active during the 
            # report period.
            if (employee_profile_info and 
                employee_profile_info.is_employee_active_anytime_in_time_period(period_start, period_end)):
                
                person_info = self.view_model_factory.get_employee_person_info(employee_user_id)
                self._write_employee(employee_user_id, person_info, employee_profile_info, employees_reported_hours)

    def _write_employee(
        self,
        employee_user_id,
        person_info,
        employee_profile_info,
        employees_reported_hours
    ):
        # If some of the necessary data does not exist, omit the employee
        if (not person_info 
            or not employee_profile_info):
            return


        row_data = self._get_hours_row_base(
                employee_user_id,
                person_info,
                employee_profile_info)
        
        user_hours = None
        if (employee_user_id in employees_reported_hours):
            user_hours = employees_reported_hours[employee_user_id]
        
        # First, let's write the hours worked
        if (employee_profile_info and employee_profile_info.pay_type == PAY_TYPE_SALARY):
            salary_hours = SALARY_EMPLOYEE_HOURS_PER_DAY * self.week_days
            if(user_hours):
                # if we have PTO or Sick time cards for salary employees, remove those hours
                salary_hours -= user_hours.paid_time_off_hours
                salary_hours -= user_hours.sick_time_hours
            row_data['work_hours'] = self._normalize_decimal_number(salary_hours)
        else:
            if user_hours:
                row_data['work_hours'] = self._normalize_decimal_number(user_hours.paid_hours)
            else:
                row_data['work_hours'] = 0.0
        self._write_row(row_data)

        if user_hours:
            if(employee_profile_info and employee_profile_info.pay_type == PAY_TYPE_HOURLY):
                # Write the hours worked over time only for hourly employees
                self._write_hours_for_type(
                    user_hours.overtime_hours,
                    OVERTIME_PAY_CODE,
                    employee_user_id,
                    person_info,
                    employee_profile_info
                )

            # Write the hours took off for vacations
            self._write_hours_for_type(
                user_hours.paid_time_off_hours,
                PAID_TIME_OFF_CODE,
                employee_user_id,
                person_info,
                employee_profile_info
            )

            # Write the hours took off for sick
            self._write_hours_for_type(
                user_hours.sick_time_hours,
                SICK_TIME_CODE,
                employee_user_id,
                person_info,
                employee_profile_info
            )

    def _write_hours_for_type(self, hours, pay_code, employee_user_id, person_info, employee_profile_info):
        if hours and hours > 0:
            row_data = self._get_hours_row_base(
                employee_user_id,
                person_info,
                employee_profile_info)
            row_data['pay_type_code'] = pay_code
            row_data['work_hours'] = self._normalize_decimal_number(hours)
            self._write_row(row_data)

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

    def _get_hours_row_base(self, employee_user_id, person_info, employee_profile_info):
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
        ap_employee_number = self.integration_provider_service.get_employee_integration_provider_external_id(
            employee_user_id,
            INTEGRATION_SERVICE_TYPE_PAYROLL,
            INTEGRATION_PAYROLL_CONNECT_PAYROLL)
        row_data['employee_number'] = ap_employee_number

        row_data['full_name'] = person_info.get_full_name()

        row_data['pay_type_code'] = self._get_employee_pay_type_code(employee_profile_info.pay_type)
        row_data['pay_rate'] = self._normalize_decimal_number(self._get_employee_pay_rate(employee_profile_info))
        
        return row_data

    def _get_employee_pay_rate(self, employee_profile_info):
        if (employee_profile_info.pay_type == PAY_TYPE_HOURLY and employee_profile_info.current_hourly_rate):
            return employee_profile_info.current_hourly_rate
        return ''

    def _get_employee_pay_type_code(self, employee_pay_type):
        if (employee_pay_type == PAY_TYPE_HOURLY):
            return 'H'
        elif (employee_pay_type == PAY_TYPE_SALARY):
            return 'S'
        else: 
            return ''

    def _normalize_decimal_number(self, decimal_number):
        result = decimal_number
        if (decimal_number == 0 or decimal_number):
            result = "{:.2f}".format(float(decimal_number))
        return result

    def _get_week_day_number(self, start, end):
        # The solution below comes from 
        # http://coding.derkeiler.com/Archive/Python/comp.lang.python/2004-09/3758.html
        dates=rrule.rruleset() # create an rrule.rruleset instance 
        dates.rrule(rrule.rrule(rrule.DAILY, dtstart=start, until=end)) 
                     # this set is INCLUSIVE of alpha and omega 
        dates.exrule(rrule.rrule(rrule.DAILY, 
                                byweekday=(rrule.SA, rrule.SU), 
                                dtstart=start)) 
        # here's where we exclude the weekend dates 
        return len(list(dates)) # there's probably a faster way to handle this 
