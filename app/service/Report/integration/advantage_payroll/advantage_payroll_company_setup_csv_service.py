from django.contrib.auth import get_user_model

from app.models.w4 import (
    W4_MARRIAGE_STATUS_SINGLE,
    W4_MARRIAGE_STATUS_MARRIED,
    W4_MARRIAGE_STATUS_MARRIED_HIGH_SINGLE
)

from app.factory.report_view_model_factory import ReportViewModelFactory

from app.service.Report.csv_report_service_base import CsvReportServiceBase

User = get_user_model()


class AdvantagePayrollCompanySetupCsvService(CsvReportServiceBase):

    def __init__(self):
        super(AdvantagePayrollCompanySetupCsvService, self).__init__()
        self.view_model_factory = ReportViewModelFactory()

    def get_report(self, company_id, outputStream):
        self._write_headers()
        self._write_company(company_id)
        self._save(outputStream)

    def _write_headers(self):
        self._write_cell('CLTNO')
        self._write_cell('EMPNO')
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
        self._write_cell('HIREDATE')
        self._write_cell('PAYCODE')
        self._write_cell('CYCLE')
        self._write_cell('SCHEDHRS')
        self._write_cell('HOURLYRATE')
        self._write_cell('SALARYAMT')
        self._write_cell('RATEDATE')
        self._write_cell('DEPT')
        self._write_cell('STATUS')
        self._write_cell('WORKSTATE')
        self._write_cell('FITSTATUS')
        self._write_cell('FITEXEMPT')
        self._write_cell('FITAMT')
        self._write_cell('SITSTATUS')
        self._write_cell('SITCODE')

    def _write_company(self, company_id):
        company_info = self.view_model_factory.get_company_info(company_id)

        users_id = self._get_all_employee_user_ids_for_company(company_id)

        # For each of them, write out his/her information
        for i in range(len(users_id)):
            self._write_employee(users_id[i], company_info)

    def _write_employee(self, employee_user_id, company_info):
        person_info = self.view_model_factory.get_employee_person_info(employee_user_id)

        # now start writing the employee row
        self._next_row()

        # [TODO]: For now, skip the below fields
        #   - CLTNO: Clint number registered with Advantage Payroll
        self._skip_cells(1)

        # [TODO]: For now, use our internal user ID as the acting EMPNO 
        #         i.e. Employee number. Until we have that in our system
        self._write_cell(employee_user_id)

        # Now write the basic personal info of the employee
        self._write_employee_basic_info(person_info)

        # Now write the employee's employment profile details
        self._write_employee_employment_profile_info(company_info)

        # Noew write the employee's w4/witholding info
        self._write_employee_w4_info(employee_user_id, company_info)

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

    def _write_employee_employment_profile_info(self, company_info):
        self._skip_cells(9)

        # [TODO]: For now, use the company address state as the employee
        #         work state
        self._write_cell(company_info.state)

    def _write_employee_w4_info(self, employee_user_id, company_info):
        w4_info = self.view_model_factory.get_employee_w4_data(employee_user_id)
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

    # To discuss
    #  * Missing Client Number
    #  * Missing Employee Number
    #  * What is "Work State"
    #  * Missing State tax witholding data
    #  * W4 missing handling of exempt selection
    #  * If W4 selects "married but withold at a higher single rate", what to fill
    #  * What do we fill into the "Department" field
