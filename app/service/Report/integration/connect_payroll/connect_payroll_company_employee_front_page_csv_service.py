import traceback

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
        INTEGRATION_PAYROLL_CONNECT_PAYROLL
    )
from app.factory.report_view_model_factory import ReportViewModelFactory

from app.service.Report.csv_report_service_base import CsvReportServiceBase
from app.service.monitoring.logging_service import LoggingService
from .tax.connect_payroll_state_tax_election_adaptor_factory import ConnectPayrollStateTaxElectionAdaptorFactory

User = get_user_model()


class ConnectPayrollCompanyEmployeeFrontPageCsvService(CsvReportServiceBase):

    ########################################################################
    ## Items of further investigations
    ## * [Employement Type] WBM: Only W-2   CP: W-2 and 1099-M
    ## * [W-4 Status] WBM: Married high rate    CP: Head of house hold
    ## * [W-4 withold state] WBM: Company State (correct?). CP: allow more options
    ## * [W-4 additional amount] WBM: additional dollar.  CP: more options
    ## * [I-9 status] WBM does not know F-1/J-1 status
    ## * [Employment Status] Does WBM include terminated employees?
    ## * [New Hire Flag] Does the NewHire flag stands for the same expectation
    ##   on WBM and CP?
    ########################################################################

    def __init__(self):
        super(ConnectPayrollCompanyEmployeeFrontPageCsvService, self).__init__()
        self.view_model_factory = ReportViewModelFactory()
        self.integration_provider_service = IntegrationProviderService()
        self.logger = LoggingService()
        self._state_tax_election_adaptor_factory = ConnectPayrollStateTaxElectionAdaptorFactory()

    def get_report(self, company_id, outputStream):
        try:
            client_id = self._get_client_number(company_id)
            if (not client_id):
                raise ValueError('The company is not properly configured to integrate with Connect Payroll service!')

            self._write_headers()
            self._write_company(company_id, client_id)
            self._save(outputStream)
        except Exception as e:
            self.logger.error('Failed to produce Connect Payroll Employee Front Page export for company "{0}"'.format(company_id))
            self.logger.error(traceback.format_exc())
            raise e

    def _get_client_number(self, company_id):
        return self.integration_provider_service.get_company_integration_provider_external_id(
            company_id,
            INTEGRATION_SERVICE_TYPE_PAYROLL,
            INTEGRATION_PAYROLL_CONNECT_PAYROLL)

    def _write_headers(self):

        # Integration Identifier
        self._write_cell('EmpNumber')
        self._write_cell('Ssn')

        # Organizational Allocation
        self._write_cell('HomeLocation')
        self._write_cell('Division')
        self._write_cell('Department')

        # Employee Name
        self._write_cell('FirstName')
        self._write_cell('MiddleName')
        self._write_cell('LastName')

        # Pay Schedule
        self._write_cell('PayFrequency')
        self._write_cell('ScheduleName')

        # Employee Address
        self._write_cell('AddressLine1')
        self._write_cell('AddressLine2')
        self._write_cell('City')
        self._write_cell('ResidentState')
        self._write_cell('ZipCode')
        self._write_cell('ZipCodeExt')

        # Employment Type
        self._write_cell('EmpType')

        # Federal Tax
        self._write_cell('FedFS')
        self._write_cell('FedExemptions')
        self._write_cell('FedAddl')
        self._write_cell('FedAmt')
        self._write_cell('WorkingIn')
        self._write_cell('WithholdIncomeTaxIn')

        # State Tax
        self._write_cell('StateFS')
        self._write_cell('StateExemptions')
        self._write_cell('StateAddlExemptions')
        self._write_cell('StateAddl')
        self._write_cell('StateAmt')
        self._write_cell('SecondStateFS')
        self._write_cell('SecondStateExemptions')
        self._write_cell('SecondStateAddlExemptions')
        self._write_cell('SecondStateAddl')
        self._write_cell('SecondStateAmt')

        # 1099-M Employee Info
        # [Remark] WBM Non-supported
        self._write_cell('ApplyFedId')

        # Employee HR Info
        self._write_cell('Email')
        self._write_cell('Birthdate')

        # Salary Data
        self._write_cell('Salary')
        self._write_cell('SalaryDate')
        self._write_cell('Rate')
        self._write_cell('RateDate')

        # Other HR Data
        self._write_cell('NewHire')
        self._write_cell('Seasonal')
        self._write_cell('HireDate')
        self._write_cell('Gender')
        self._write_cell('Primary Phone')
        self._write_cell('J1F1Visa')
        self._write_cell('VisaDate')
        self._write_cell('Status')
        self._write_cell('StatusDate')
        self._write_cell('StatusReason')

        # Other Tax Data
        # [Remark] WBM Non-supported
        self._write_cell('SsExempt')
        self._write_cell('MedcExempt')
        self._write_cell('FutaExempt')
        self._write_cell('FutaExemptReason')
        self._write_cell('SuiExempt')
        self._write_cell('NonUsAddress')
        self._write_cell('PostalCode1')
        self._write_cell('PostalCode2')
        self._write_cell('PostalCode3')
        self._write_cell('Country')

    def _write_company(self, company_id, client_id):
        user_ids = self._get_all_employee_user_ids_for_company(company_id)

        # For each of them, write out his/her information
        for i in range(len(user_ids)):
            self._write_employee(user_ids[i], company_id, client_id)

    def _write_employee(self, employee_user_id, company_id, client_id):
        employee_data_context = _EmployeeDataContext(employee_user_id, company_id)

        if not employee_data_context.user_completed_onboarding():
            self.logger.warn('Skipping employee "{0}": Onboarding not complete.'.format(employee_user_id))
            return
        if (not employee_data_context.has_complete_data()):
            self.logger.warn('Skipping employee "{0}": Missing necessary information'.format(employee_user_id))
            return

        # now start writing the employee row
        self._next_row()

        self._write_integration_info(employee_data_context)
        self._write_organizational_allocation_info(employee_data_context)
        self._write_employee_name(employee_data_context)
        self._write_employee_pay_schedule(employee_data_context)
        self._write_employee_address(employee_data_context)
        self._write_employment_type(employee_data_context)
        self._write_federal_tax_info(employee_data_context)
        self._write_state_tax_info(employee_data_context)
        self._write_1099M_data(employee_data_context)
        self._write_employee_HR_info(employee_data_context)
        self._write_employee_salary_data(employee_data_context)
        self._write_employee_other_HR_data(employee_data_context)

    def _write_integration_info(self, employee_data_context):
        self._write_cell(employee_data_context.employee_number)
        self._write_cell(employee_data_context.person_info.ssn)

    def _write_organizational_allocation_info(self, employee_data_context):
        # Skippng 'HomeLocation' as it is not used
        self._skip_cells(1)

        employee_profile_info = employee_data_context.employee_profile_info
        
        if (employee_profile_info.division and employee_profile_info.division.code):
            self._write_cell(employee_profile_info.division.code)
        else:
            self._skip_cells(1)

        if (employee_profile_info.department and employee_profile_info.department.code):
            self._write_cell(employee_profile_info.department.code)
        else:
            self._skip_cells(1)

    def _write_employee_name(self, employee_data_context):
        person_info = employee_data_context.person_info

        self._write_cell(person_info.first_name)
        self._write_cell(person_info.middle_name)
        self._write_cell(person_info.last_name)

    def _write_employee_pay_schedule(self, employee_data_context):
        employee_profile_info = employee_data_context.employee_profile_info

        mapped_paycode = self._get_pay_cycle_code(employee_profile_info.pay_cycle)
        if (not mapped_paycode):
            self.logger.warn('[Data Issue] Employee "{0}": has invalid pay-code'.format(employee_data_context.employee_user_id))
            self._skip_cells(1)
        else:
            self._write_cell(mapped_paycode)

        # Skip the 'ScheduleName' field
        self._skip_cells(1)

    def _get_pay_cycle_code(self, pay_cycle):
        if (pay_cycle == PERIOD_WEEKLY):
            return 'Weekly'
        elif(pay_cycle == PERIOD_BIWEEKLY):
            return 'Biweekly'
        elif(pay_cycle == PERIOD_SEMIMONTHLY):
            return 'Semi-Monthly'
        elif(pay_cycle == PERIOD_MONTHLY):
            return 'Monthly'
        else:
            return ''

    def _write_employee_address(self, employee_data_context):
        person_info = employee_data_context.person_info
        self._write_cell(person_info.address1)
        self._write_cell(person_info.address2)
        self._write_cell(person_info.city)
        self._write_cell(person_info.state)
        self._write_cell(person_info.zipcode)

        # Skip the zip extension, not supported
        self._skip_cells(1)

    def _write_employment_type(self, employee_data_context):
        # [Remark]: We only support W2 employee (?)
        self._write_cell('W2')

    def _write_federal_tax_info(self, employee_data_context):
        w4_info = employee_data_context.w4_info
        company_info = employee_data_context.company_info

        status_code = self._get_w4_marriage_status_code(w4_info.marriage_status)

        self._write_cell(status_code)
        self._write_cell(w4_info.total_points)
        self._write_cell('A')
        self._write_cell(w4_info.extra_amount)
        self._write_cell(company_info.state)
        self._write_cell(company_info.state)

    def _get_w4_marriage_status_code(self, marriage_status):
        if (marriage_status == W4_MARRIAGE_STATUS_SINGLE):
            return 'S'
        elif(marriage_status == W4_MARRIAGE_STATUS_MARRIED):
            return 'M'
        elif(marriage_status == W4_MARRIAGE_STATUS_MARRIED_HIGH_SINGLE):
            return 'H'
        else:
            return ''

    def _write_state_tax_info(self, employee_data_context):
        w4_info = employee_data_context.w4_info
        state_tax_info = employee_data_context.state_tax_info

        # This limits how many state elections CP can take and hence
        # we can output
        export_limit = 2
        counter = 0

        all_state_elections = state_tax_info.get_all_state_elections()

        for state in all_state_elections:
            if (counter >= export_limit):
                break
            adaptor = self._state_tax_election_adaptor_factory.get_adaptor(state, all_state_elections[state])
            if (adaptor):
                self._write_cell(adaptor.get_filing_status())
                self._write_cell(adaptor.get_total_exemptions())
                self._write_cell(adaptor.get_additional_exemptions())
                self._write_cell(adaptor.get_additional_amount_code())
                self._write_cell(adaptor.get_additional_amount())

                counter = counter + 1

        # Skip any set of fields that the employee does not have data to fill
        # E.g. secondary state witholding
        self._skip_cells((export_limit - counter) * 5)

    def _write_1099M_data(self, employee_data_context):
        # [Remark]: WBM does not support 1099-M
        self._skip_cells(1)

    def _write_employee_HR_info(self, employee_data_context):
        person_info = employee_data_context.person_info
        self._write_cell(person_info.email)
        self._write_cell(self._get_date_string(person_info.birth_date))

    def _write_employee_salary_data(self, employee_data_context):
        employee_profile_info = employee_data_context.employee_profile_info
        pay_type = employee_profile_info.pay_type
        if (pay_type == PAY_TYPE_HOURLY):
            self._skip_cells(2)
            self._write_cell(self._normalize_decimal_number(employee_profile_info.current_hourly_rate))
            self._write_cell(self._get_date_string(employee_profile_info.compensation_effective_date))
        elif (pay_type == PAY_TYPE_SALARY):
            self._write_cell(self._normalize_decimal_number(employee_profile_info.annual_salary))
            self._write_cell(self._get_date_string(employee_profile_info.compensation_effective_date))
            self._skip_cells(2)
        else:
            self.logger.warn('Skipping data for employee "{0}": Invalid pay type.'.format(employee_data_context.employee_user_id))
            self._skip_cells(4)

    def _write_employee_other_HR_data(self, employee_data_context):
        employee_profile_info = employee_data_context.employee_profile_info
        person_info = employee_data_context.person_info

        self._write_cell(employee_profile_info.new_employee)
        # [Remark]: Seasonal is not supported on WBM and seems to not be used by CP
        self._skip_cells(1)
        self._write_cell(self._get_date_string(employee_profile_info.hire_date))
        self._write_cell(person_info.gender)

        if (len(person_info.phones) > 0):
            phone = person_info.phones[0]
            self._write_cell(phone['number'])
        else:
            self._skip_cells(1)

        # [Remark]: Skip all J1/F1 Visa 
        self._skip_cells(2)

        code_and_date = self._get_employement_status_code_and_date(employee_profile_info)
        if (not code_and_date):
            self.logger.warn('Skipping data for employee "{0}": Invalid employment status'.format(employee_data_context.employee_user_id))
            self._skip_cells(2)
        else:
            self._write_cell(code_and_date['code'])
            self._write_cell(code_and_date['date'])

        # [Remark]: Skip the status reason
        self._skip_cells(1)

    def _get_employement_status_code_and_date(self, employee_profile_info):
        employment_status = employee_profile_info.employment_status
        if (employment_status == EMPLOYMENT_STATUS_ACTIVE):
            return {
                'code': 'Active',
                'date': self._get_date_string(employee_profile_info.hire_date)
            }
        elif (employment_status == EMPLOYMENT_STATUS_TERMINATED):
            return {
                'code': 'Terminated',
                'date': self._get_date_string(employee_profile_info.end_date)
            }
        else:
            return None

    def _write_other_tax_data(self, employee_data_context):
        # [Remark] WBM Non-supported
        # [Remark] CP does not seem to use 
        self._skip_cells(10)

    def _normalize_decimal_number(self, decimal_number):
        result = decimal_number
        if (decimal_number == 0 or decimal_number):
            result = "{:.2f}".format(float(decimal_number))
        return result


class _EmployeeDataContext(object):
    _view_model_factory = ReportViewModelFactory()
    _integration_provider_service = IntegrationProviderService()

    def __init__(self, employee_user_id, company_id):
        self.employee_user_id = employee_user_id
        self.company_id = company_id

        self.w4_info = self._view_model_factory.get_employee_w4_data(employee_user_id)
        self.state_tax_info = self._view_model_factory.get_employee_state_tax_data(employee_user_id)
        self.company_info = self._view_model_factory.get_company_info(company_id)
        self.person_info = self._view_model_factory.get_employee_person_info(employee_user_id)
        self.employee_profile_info = self._view_model_factory.get_employee_employment_profile_data(
                                        employee_user_id,
                                        company_id)

        # Employee Number, this comes from the CP system.
        self.employee_number = self._integration_provider_service.get_employee_integration_provider_external_id(
            employee_user_id,
            INTEGRATION_SERVICE_TYPE_PAYROLL,
            INTEGRATION_PAYROLL_CONNECT_PAYROLL)

    def user_completed_onboarding(self):
        if not self.w4_info or not self.w4_info.total_points: 
            comp_user = CompanyUser.objects.get(user=self.employee_user_id, company_user_type=USER_TYPE_EMPLOYEE, company=self.company_id)
            return not comp_user.new_employee
        return True

    def has_complete_data(self):
        return self.user_completed_onboarding() \
            and self.state_tax_info \
            and self.employee_number \
            and self.company_info \
            and self.person_info \
            and self.employee_profile_info
