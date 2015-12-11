import xlwt

from report_export_view_base import ReportExportViewBase

class ExcelExportViewBase(ReportExportViewBase):

    _book = None
    _current_work_sheet = None

    _current_column = 0
    _current_row = 0

    def _init(self):
        if self._book is None:
            self._book = xlwt.Workbook(encoding='utf8')
        return

    def _start_work_sheet(self, name):
        self._current_work_sheet = self._book.add_sheet(name)
        self._reset_position()
        return

    def _reset_position(self):
        self._current_column = 0
        self._current_row = 0
        return

    def _save(self, response):
        self._book.save(response)
        return

    def _get_employee_person(self, user_id):
        try:
            person_list = Person.objects.filter(user=user_id, relationship='self')
            if person_list:
                return person_list[0]
            return None
        except Person.DoesNotExist:
            return None

    def _write_cell(self, value, value_format=None):
        if (value_format):
            self._current_work_sheet.write(
                self._current_row,
                self._current_column,
                value,
                value_format)
        else:
            self._current_work_sheet.write(
                self._current_row,
                self._current_column,
                value)

        self._current_column = self._current_column + 1
        return

    def _skip_cells(self, num_cells):
        self._current_column = self._current_column + num_cells
        return

    def _next_row(self):
        self._current_row = self._current_row + 1
        self._current_column = 0
        return

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
