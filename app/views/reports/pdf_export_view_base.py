from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth  

from report_export_view_base import ReportExportViewBase

class PdfExportViewBase(ReportExportViewBase):
    _page_margin_left_right = 20
    _page_margin_top_bottom = 30
    _line_height = 10
    _font_family = 'Helvetica'
    _font_size = 10
    _line_thickness = 1

    _width = 0
    _height = 0
    _write_area_height = 0
    _write_area_width = 0

    _current_X = 0
    _current_Y = 0

    _canvas = None

    def _init_canvas(self, response):
        if self._canvas is None: 
            self._canvas = canvas.Canvas(response, pagesize=letter)
            self._canvas.setFont(self._font_family, self._font_size)
            self._width, self._height = letter
            self._write_area_width = self._width - self._page_margin_left_right * 2.0
            self._write_area_height = self._height - self._page_margin_top_bottom * 2.0
        return

    def _translate_X(self, x):
        return self._page_margin_left_right + x

    def _translate_Y(self, y):
        return self._height - self._page_margin_top_bottom - y

    def _start_new_page(self):
        self._canvas.showPage()
        self._current_X = 0
        self._current_Y = 0
        return

    def _get_text_width(self, text):
        return stringWidth(text, self._font_family, self._font_size)

    def _save(self):
        self._canvas.save()
        return

    def _write_text(self, text, trail_spacing=10):
        self._canvas.drawString(self._translate_X(self._current_X), self._translate_Y(self._current_Y), text)
        self._current_X = self._current_X + self._get_text_width(text) + trail_spacing
        return

    def _write_text_fix_width(self, text, text_width):
        self._canvas.drawString(self._translate_X(self._current_X), self._translate_Y(self._current_Y), text)
        self._current_X = self._current_X + text_width
        return

    def _start_new_line(self):
        self._current_X = 0
        self._current_Y = self._current_Y + self._line_height
        if self._current_Y > self._write_area_height:
            self._start_new_page()
        return

    def _write_line_uniform_width(self, text_items=None):    
        if text_items is None or len(text_items) <= 0:
            return

        if self._current_X > 0:
            self._start_new_line()

        # For now, use simple uniform spacing
        num_items = len(text_items)
        segment_length = self._write_area_width / num_items

        for text in text_items:
            self._write_text_fix_width(text, segment_length)

        # End this line and move to next
        self._start_new_line()

        return 

    def _write_line(self, text_items=None):
        if text_items is None or len(text_items) <= 0:
            return

        if self._current_X > 0:
            self._start_new_line()

        for text in text_items:
            self._write_text(text)

        # End this line and move to next
        self._start_new_line()

        return 

    def _draw_line(self):
        if self._current_X > 0:
            self._start_new_line()

        self._canvas.line(
            self._translate_X(0), \
            self._translate_Y(self._current_Y), \
            self._translate_X(self._write_area_width), \
            self._translate_Y(self._current_Y + self._line_thickness))

        self._start_new_line()

        return
