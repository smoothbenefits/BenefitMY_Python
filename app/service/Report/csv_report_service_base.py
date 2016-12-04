import csv

from report_service_base import ReportServiceBase


class CsvReportServiceBase(ReportServiceBase):
    def __init__(self):
        self._rows = []
        self._rows.append([])

    def _save(self, output_stream):
        writer = csv.writer(output_stream)

        for row in self._rows:
            writer.writerow(row)

        return

    def _write_cell(self, value):
        self._rows[-1].append(value)
        return

    def _skip_cells(self, num_cells):
        for i in range(num_cells):
            self._write_cell('')
        return

    def _next_row(self):
        self._rows.append([])
        return