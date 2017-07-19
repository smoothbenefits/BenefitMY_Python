from report_service_base import ReportServiceBase
from app.service.Report.pdf_compose_service import PdfComposeService


class PdfReportServiceBase(ReportServiceBase):
    def __init__(self):
        self.pdf_composer = PdfComposeService()

    def _normalize_dollar_amount(self, text):
        result = text
        if (text is not None):
            result = "${:.2f}".format(float(text))
        return result
