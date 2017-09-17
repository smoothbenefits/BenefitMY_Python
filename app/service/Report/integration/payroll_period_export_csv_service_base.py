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
        INTEGRATION_SERVICE_TYPE_PAYROLL
    )
from app.service.Report.csv_report_service_base import CsvReportServiceBase

User = get_user_model()

EARNING_TYPE_HOURLY = PAY_TYPE_HOURLY
EARNING_TYPE_SALARY = PAY_TYPE_SALARY
EARNING_TYPE_OVERTIME = 'Overtime'
EARNING_TYPE_PTO = 'PTO'
EARNING_TYPE_SICK_TIME = 'SICK'
EARNING_TYPE_HOLIDAY = 'HOLIDAY'
EARNING_TYPE_UNPAID_LEAVE = 'UnpaidLeave'

SALARY_EMPLOYEE_HOURS_PER_DAY = 8


class PayrollPeriodExportCsvServiceBase(CsvReportServiceBase):
    
    ''' Big assumptions and TODOs
        * The expectation for this export is weekly
        * Though salary rate exported here is per pay period
        * Personal Leave is the only card type that does not count towards hours reported
        * Company Holiday is counted as 8 hours
        * Only export employee's who is at least partially active in the period
        * The report does not try to prorate if employee was terminated during the period. 
    '''

    def __init__(self):
        super(PayrollPeriodExportCsvServiceBase, self).__init__()
        self.view_model_factory = ReportViewModelFactory()
        self.time_punch_card_service = TimePunchCardService()
        self.integration_provider_service = IntegrationProviderService()
        self.week_days = 0

    #########################################
    ## Abstract methods - Begin
    #########################################

    def _get_integration_payroll_service_name(self):
        raise NotImplementedError()

    def _needs_write_header_row(self):
        raise NotImplementedError()

    def _write_headers(self):
        raise NotImplementedError()

    def _get_pay_code(self, earning_type):
        raise NotImplementedError()

    def _get_pay_name(self, earning_type):
        raise NotImplementedError()

    def _write_row(self, row_data):
        raise NotImplementedError()

    def _get_employee_data_rows(
        self,
        employee_user_id,
        person_info,
        employee_profile_info,
        employees_reported_hours
    ):
        raise NotImplementedError()

    #########################################
    ## Abstract methods - End
    #########################################

    def get_report(self, company_id, period_start, period_end, outputStream):
        client_id = self._get_client_number(company_id)
        if (not client_id):
            raise ValueError('The company is not properly configured to integrate with Payroll service!')
        self.week_days = self._get_week_day_number(period_start, period_end)

        if (self._needs_write_header_row()):
            self._write_headers()

        self._write_company(company_id, period_start, period_end)
        self._save(outputStream)

    def _get_client_number(self, company_id):
        service_name = self._get_integration_payroll_service_name()
        return self.integration_provider_service.get_company_integration_provider_external_id(
            company_id,
            INTEGRATION_SERVICE_TYPE_PAYROLL,
            service_name)

    def _write_company(self, company_id, period_start, period_end):
        user_ids = self._get_all_employee_user_ids_for_company(company_id)

        # Get the time tracking data for the company, for the date period
        # specified
        employees_reported_hours = self.time_punch_card_service.get_company_users_reported_hours_by_date_range(
            company_id, period_start, period_end)

        company_info = self.view_model_factory.get_company_info(company_id)
        company_payroll_id = self._get_client_number(company_id)

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
                self._write_employee(employee_user_id, person_info, company_info, company_payroll_id, employee_profile_info, employees_reported_hours)

    def _write_employee(
        self,
        employee_user_id,
        person_info,
        company_info,
        company_payroll_id,
        employee_profile_info,
        employees_reported_hours
    ):
        rows = self._get_employee_data_rows(
            employee_user_id,
            person_info,
            company_info,
            company_payroll_id,
            employee_profile_info,
            employees_reported_hours
        )

        for row in rows:
            self._write_row(row)

    def _get_hours_by_earning_type(self, earning_type, employee_hours):
        if (earning_type == EARNING_TYPE_HOURLY):
            if employee_hours:
                return self._normalize_decimal_number(employee_hours.paid_hours)
            else:
                return 0.0
        elif (earning_type == EARNING_TYPE_SALARY):
            salary_hours = SALARY_EMPLOYEE_HOURS_PER_DAY * self.week_days
            if(employee_hours):
                # if we have PTO, Holiday, unpaid_leave or Sick time cards for salary employees, remove those hours
                salary_hours -= employee_hours.paid_time_off_hours
                salary_hours -= employee_hours.holiday_hours
                salary_hours -= employee_hours.sick_time_hours
                salary_hours -= employee_hours.unpaid_hours
            return self._normalize_decimal_number(salary_hours)
        elif (earning_type == EARNING_TYPE_OVERTIME):
            return employee_hours.overtime_hours
        elif (earning_type == EARNING_TYPE_PTO):
            return employee_hours.paid_time_off_hours
        elif (earning_type == EARNING_TYPE_SICK_TIME):
            return employee_hours.sick_time_hours
        elif (earning_type == EARNING_TYPE_HOLIDAY):
            return employee_hours.holiday_hours
        elif (earning_type == EARNING_TYPE_UNPAID_LEAVE):
            return employee_hours.unpaid_hours

    def _get_employee_pay_rate(self, employee_profile_info):
        if (employee_profile_info.pay_type == PAY_TYPE_HOURLY and employee_profile_info.current_hourly_rate):
            return employee_profile_info.current_hourly_rate
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
