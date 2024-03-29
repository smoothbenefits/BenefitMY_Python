from django.contrib.auth import get_user_model

from app.models.w4 import (
    W4_MARRIAGE_STATUS_SINGLE,
    W4_MARRIAGE_STATUS_MARRIED,
    W4_MARRIAGE_STATUS_MARRIED_HIGH_SINGLE
)
from app.models.company_user import CompanyUser, USER_TYPE_EMPLOYEE
from app.models.sys_period_definition import (
    PERIOD_WEEKLY,
    PERIOD_BIWEEKLY,
    PERIOD_SEMIMONTHLY,
    PERIOD_MONTHLY
)
from app.models.employee_profile import (
    EMPLOYMENT_STATUS_ACTIVE,
    EMPLOYMENT_STATUS_TERMINATED
)

from app.service.compensation_service import (
    PAY_TYPE_HOURLY,
    PAY_TYPE_SALARY
)
from app.service.integration.integration_provider_service import (
        IntegrationProviderService,
        INTEGRATION_SERVICE_TYPE_PAYROLL,
        INTEGRATION_PAYROLL_ADVANTAGE_PAYROLL
    )
from app.factory.report_view_model_factory import ReportViewModelFactory

from app.service.Report.csv_report_service_base import CsvReportServiceBase

User = get_user_model()


class AdvantagePayrollCompanySetupCsvService(CsvReportServiceBase):

    def __init__(self):
        super(AdvantagePayrollCompanySetupCsvService, self).__init__()
        self.view_model_factory = ReportViewModelFactory()
        self.integration_provider_service = IntegrationProviderService()

    def get_report(self, company_id, outputStream):
        ap_client_id = self._get_ap_client_number(company_id)
        if (not ap_client_id):
            raise ValueError('The company is not properly configured to integrate with Advantage Payroll service!')

        self._write_headers()
        self._write_company(company_id, ap_client_id)
        self._save(outputStream)

    def _get_ap_client_number(self, company_id):
        return self.integration_provider_service.get_company_integration_provider_external_id(
            company_id,
            INTEGRATION_SERVICE_TYPE_PAYROLL,
            INTEGRATION_PAYROLL_ADVANTAGE_PAYROLL)

    def _write_headers(self):

        # IDs
        self._write_cell('CLTNO')
        self._write_cell('EMPNO')

        # Basic Info
        self._write_cell('FIRSTNAME')
        self._write_cell('LASTNAME')
        self._write_cell('BIRTHDATE')
        self._write_cell('SEX')
        self._write_cell('SSN')
        self._write_cell('ADDR1')
        self._write_cell('ADDR2')
        self._write_cell('CITY')
        self._write_cell('STATE')
        self._write_cell('ZIPCODE')

        # Employment Profile
        self._write_cell('HIREDATE')
        self._write_cell('CYCLE')
        self._write_cell('DEPT')
        self._write_cell('STATUS')
        self._write_cell('WORKSTATE')

        # Compensation
        self._write_cell('SCHEDHRS')
        self._write_cell('PAYCODE')
        self._write_cell('HOURLYRATE')
        self._write_cell('SALARYAMT')
        self._write_cell('RATEDATE')

        # Tax Witholding
        self._write_cell('FITSTATUS')
        self._write_cell('FITEXEMPT')
        self._write_cell('FITAMT')
        self._write_cell('SITSTATUS')
        self._write_cell('SITCODE')

    def _write_company(self, company_id, ap_client_id):
        user_ids = self._get_all_employee_user_ids_for_company(company_id)

        # For each of them, write out his/her information
        for i in range(len(user_ids)):
            self._write_employee(user_ids[i], company_id, ap_client_id)

    def _user_completed_onboarding(self, company_id, user_id, w4_info):
        if not w4_info or not w4_info.total_points: 
            comp_user = CompanyUser.objects.get(user=user_id, company_user_type=USER_TYPE_EMPLOYEE, company=company_id)
            return not comp_user.new_employee
        return True

    def _write_employee(self, employee_user_id, company_id, ap_client_id):
        w4_info = self.view_model_factory.get_employee_w4_data(employee_user_id)
        if not self._user_completed_onboarding(company_id, employee_user_id, w4_info):
            return
        company_info = self.view_model_factory.get_company_info(company_id)
        person_info = self.view_model_factory.get_employee_person_info(employee_user_id)

        # now start writing the employee row
        self._next_row()

        # Client number, this comes from the AP system
        self._write_cell(ap_client_id)

        # Employee Number, this comes from the AP system.
        ap_employee_number = self.integration_provider_service.get_employee_integration_provider_external_id(
            employee_user_id,
            INTEGRATION_SERVICE_TYPE_PAYROLL,
            INTEGRATION_PAYROLL_ADVANTAGE_PAYROLL)
        self._write_cell(ap_employee_number)

        # Now write the basic personal info of the employee
        self._write_employee_basic_info(person_info)

        # Now write the employee's employment profile details
        self._write_employee_employment_profile_info(employee_user_id, company_info)

        # Noew write the employee's w4/witholding info
        self._write_employee_w4_info(company_info, w4_info)

    def _write_employee_basic_info(self, person_info):
        self._write_cell(person_info.first_name)
        self._write_cell(person_info.last_name)
        self._write_cell(self._get_date_string(person_info.birth_date))
        self._write_cell(person_info.gender)
        self._write_cell(person_info.ssn)
        self._write_cell(person_info.address1)
        self._write_cell(person_info.address2)
        self._write_cell(person_info.city)
        self._write_cell(person_info.state)
        self._write_cell(person_info.zipcode)

    def _write_employee_employment_profile_info(self, user_ids, company_info):
        employee_profile_info = self.view_model_factory.get_employee_employment_profile_data(
                                    user_ids,
                                    company_info.company_id)

        if (not employee_profile_info):
            self._skip_cells(10)
            return

        # Profile
        self._write_cell(self._get_date_string(employee_profile_info.hire_date))
        self._write_cell(self._get_pay_cycle_code(employee_profile_info.pay_cycle))

        # [TODO]: For now, skip the department info
        self._skip_cells(1)
        self._write_cell(self._get_employment_status_code(employee_profile_info.employment_status))

        # [TODO]: For now, use the company address state as the employee
        #         work state
        self._write_cell(company_info.state)

        # Compensation
        self._write_cell(self._normalize_decimal_number(employee_profile_info.projected_hours_per_pay_cycle))
        self._write_cell(self._get_employee_pay_type_code(employee_profile_info.pay_type))
        self._write_cell(self._normalize_decimal_number(employee_profile_info.current_hourly_rate))
        self._write_cell(self._get_employee_current_pay_period_salary(employee_profile_info))
        self._write_cell(self._get_date_string(employee_profile_info.compensation_effective_date))

    def _write_employee_w4_info(self, company_info, w4_info):
        if (w4_info):
            status_code = self._get_w4_marriage_status_code(w4_info.marriage_status)

            self._write_cell(status_code)
            self._write_cell(w4_info.total_points)
            self._write_cell(w4_info.extra_amount)

            # [TODO]: For now, use the federal w4 info to fill state fields
            # [TODO]: For now, use the company state for the state withold code
            self._write_cell(status_code)
            self._write_cell(company_info.state)

        else:
            self._skip_cells(5)

    def _get_w4_marriage_status_code(self, marriage_status):
        if (marriage_status == W4_MARRIAGE_STATUS_SINGLE):
            return 'S'
        elif(marriage_status == W4_MARRIAGE_STATUS_MARRIED):
            return 'M'
        elif(marriage_status == W4_MARRIAGE_STATUS_MARRIED_HIGH_SINGLE):
            return 'S'
        else:
            return ''

    def _get_pay_cycle_code(self, pay_cycle):
        if (pay_cycle == PERIOD_WEEKLY):
            return 'W'
        elif(pay_cycle == PERIOD_BIWEEKLY):
            return 'B'
        elif(pay_cycle == PERIOD_SEMIMONTHLY):
            return 'S'
        elif(pay_cycle == PERIOD_MONTHLY):
            return 'M'
        else:
            return ''

    def _get_employment_status_code(self, employment_status):
        if (employment_status == EMPLOYMENT_STATUS_ACTIVE):
            return 'A'
        elif (employment_status == EMPLOYMENT_STATUS_TERMINATED):
            return 'T'
        else:
            return ''

    def _get_employee_pay_type_code(self, employee_pay_type):
        if (employee_pay_type == PAY_TYPE_HOURLY):
            return 'H'
        elif (employee_pay_type == PAY_TYPE_SALARY):
            return 'S'
        else:
            return ''

    def _get_employee_current_pay_period_salary(self, employee_profile_info):
        if (employee_profile_info.pay_type == PAY_TYPE_HOURLY):
            return 0
        else:
            return self._normalize_decimal_number(employee_profile_info.current_pay_period_salary)

    def _normalize_decimal_number(self, decimal_number):
        result = decimal_number
        if (decimal_number == 0 or decimal_number):
            result = "{:.2f}".format(float(decimal_number))
        return result

    # To discuss
    #  * Missing Client Number
    #  * Missing Employee Number
    #  * What is "Work State"
    #  * Missing State tax witholding data
    #  * W4 missing handling of exempt selection
    #  * If W4 selects "married but withold at a higher single rate", what to fill
    #  * What do we fill into the "Department" field
