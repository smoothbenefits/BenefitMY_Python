from datetime import date

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
        INTEGRATION_PAYROLL_ADVANTAGE_PAYROLL
    )
from app.service.Report.csv_report_service_base import CsvReportServiceBase

User = get_user_model()


class AdvantagePayrollPeriodExportCsvService(CsvReportServiceBase):
    
    ''' Big assumptions and TODOs
        * The expectation for this export is weekly
        * Though salary rate exported here is per pay period
        * Personal Leave is the only card type that does not count towards hours reported
        * Company Holiday is counted as 8 hours
        * Only export employee's who is at least partially active in the period
        * The report does not try to prorate if employee was terminated during the period. 
    '''

    def __init__(self):
        super(AdvantagePayrollPeriodExportCsvService, self).__init__()
        self.view_model_factory = ReportViewModelFactory()
        self.time_punch_card_service = TimePunchCardService()
        self.integration_provider_service = IntegrationProviderService()

    def get_report(self, company_id, period_start, period_end, outputStream):
        ap_client_id = self._get_ap_client_number(company_id)
        if (not ap_client_id):
            raise ValueError('The company is not properly configured to integrate with Advantage Payroll service!')

        self._write_company(company_id, period_start, period_end)
        self._save(outputStream)

    def _get_ap_client_number(self, company_id):
        return self.integration_provider_service.get_company_integration_provider_external_id(
            company_id,
            INTEGRATION_SERVICE_TYPE_PAYROLL,
            INTEGRATION_PAYROLL_ADVANTAGE_PAYROLL)

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
                export_data = self._get_export_data(
                    employee_user_id,
                    person_info,
                    employee_profile_info,
                    employees_reported_hours)
                if (export_data):
                    self._write_employee(export_data)

    def _write_employee(self, export_data):
        self._write_cell(export_data['employee_number'])
        self._write_cell(export_data['full_name'])
        self._write_cell(export_data['pay_type_code'])
        self._write_cell(export_data['pay_rate'])
        self._write_cell(export_data['work_hours'])
        self._write_cell(export_data['division'])
        self._write_cell(export_data['department'])
        self._write_cell(export_data['job'])

        # move to next row
        self._next_row()

    def _get_export_data(self, employee_user_id, person_info, employee_profile_info, employees_reported_hours):
        # If some of the necessary data does not exist, omit the employee
        if (not person_info 
            or not employee_profile_info):
            return None

        # Per discussion with AP, the time tracking/payrol reporting
        # can omit salaried employees for now
        if (employee_profile_info):
            if (employee_profile_info.pay_type == PAY_TYPE_SALARY):
                return None

        export_data = {
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
            INTEGRATION_PAYROLL_ADVANTAGE_PAYROLL)
        export_data['employee_number'] = ap_employee_number

        export_data['full_name'] = person_info.get_full_name()
        export_data['ssn'] = person_info.ssn

        export_data['pay_type_code'] = self._get_employee_pay_type_code(employee_profile_info.pay_type)
        export_data['pay_rate'] = self._normalize_decimal_number(self._get_employee_pay_rate(employee_profile_info))

        if (employee_user_id in employees_reported_hours):
            work_hours = employees_reported_hours[employee_user_id].paid_hours
            export_data['work_hours'] = self._normalize_decimal_number(work_hours)

        return export_data

    def _get_employee_pay_rate(self, employee_profile_info):
        if (employee_profile_info.current_pay_period_salary):
            return employee_profile_info.current_pay_period_salary
        elif (employee_profile_info.current_hourly_rate):
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
