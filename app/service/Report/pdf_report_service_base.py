from report_service_base import ReportServiceBase


class PdfReportServiceBase(ReportServiceBase):
    def __init__(self):
        pass

    def _normalize_dollar_amount(self, text):
        result = text
        if (text is not None):
            result = "${:.2f}".format(float(text))
        return result
