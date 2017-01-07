from django.contrib.auth import get_user_model

from app.models.employee_profile import (
    EMPLYMENT_STATUS_ACTIVE,
    EMPLYMENT_STATUS_TERMINATED
)
from app.service.compensation_service import (
    PAY_TYPE_HOURLY,
    PAY_TYPE_SALARY
)

from app.factory.report_view_model_factory import ReportViewModelFactory

from app.service.time_tracking_service import TimeTrackingService
from app.service.Report.csv_report_service_base import CsvReportServiceBase

User = get_user_model()


class AdvantagePayrollPeriodExportCsvService(CsvReportServiceBase):

    def __init__(self):
        super(AdvantagePayrollPeriodExportCsvService, self).__init__()
        self.view_model_factory = ReportViewModelFactory()
        self.time_tracking_service = TimeTrackingService()

    def get_report(self, company_id, outputStream):
        self._write_company(company_id)
        self._save(outputStream)

    def _write_company(self, company_id):
        users_id = self._get_all_employee_user_ids_for_company(company_id)

        # For each of them, write out his/her information
        for i in range(len(users_id)):
            self._write_employee(users_id[i], company_id)

    def _write_employee(self, employee_user_id, company_id):
        person_info = self.view_model_factory.get_employee_person_info(employee_user_id)
        employee_profile_info = self.view_model_factory.get_employee_employment_profile_data(
                                    employee_user_id,
                                    company_id)

        export_data = self._get_export_data(person_info, employee_profile_info)

        self._write_cell(export_data['employee_number'])
        self._write_cell(export_data['full_name'])
        self._write_cell(export_data['pay_type_code'])
        self._write_cell(export_data['pay_rate'])
        self._write_cell(export_data['work_hours'])
        self._write_cell(export_data['division'])
        self._write_cell(export_data['department'])
        self._write_cell(export_data['job'])
        self._write_cell(export_data['ssn'])

        # move to next row
        self._next_row()

    def _get_export_data(self, person_info, employee_profile_info):
        export_data = {
            'employee_number': '',
            'full_name': '',
            'pay_type_code': '',
            'pay_rate': '',
            'work_hours': '',
            'division': '',
            'department': '',
            'job': '',
            'ssn': ''
        }

        if (person_info):
            export_data['full_name'] = person_info.get_full_name()
            export_data['ssn'] = person_info.ssn

        if (employee_profile_info):
            export_data['employee_number'] = employee_profile_info.employee_number
            export_data['pay_type_code'] = self._get_employee_pay_type_code(employee_profile_info.pay_type)
            export_data['pay_rate'] = self._normalize_decimal_number(self._get_employee_pay_rate(employee_profile_info))

        export_data['work_hours'] = self._normalize_decimal_number(20.56)

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
