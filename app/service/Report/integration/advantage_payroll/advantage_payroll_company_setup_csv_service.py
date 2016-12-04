from django.contrib.auth import get_user_model

from app.service.Report.csv_report_service_base import CsvReportServiceBase

User = get_user_model()


class AdvantagePayrollCompanySetupCsvService(CsvReportServiceBase):

    def get_report(self, company_id, outputStream):
        self._write_headers()
        self._write_company(company_id)
        self._save(outputStream)

    def _write_headers(self):
        self._write_cell('ClitNo')
        self._write_cell('FirstName')
        self._skip_cells(2)
        self._write_cell('LastName')
        self._next_row()

    def _write_company(self, company_id):
        self._write_cell('BenefitMy Ltd.')
        self._write_cell('Jeff')
        self._skip_cells(2)
        self._write_cell('Zhang')
