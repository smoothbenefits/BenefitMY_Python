import xlwt

from report_export_view_base import ReportExportViewBase

class ExcelExportViewBase(ReportExportViewBase):

    ''' Sadly Python does not support the ++ operator, or else we don't need
        this below helper to keep track of the next column number for writing
        individule field
    '''
    def _write_field(self, excelSheet, row_num, col_num, value, value_format=None):
        if (value_format):
            excelSheet.write(row_num, col_num, value, value_format)
        else:
            excelSheet.write(row_num, col_num, value)
        return col_num + 1
