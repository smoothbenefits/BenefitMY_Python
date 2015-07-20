from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth

from report_export_view_base import ReportExportViewBase

class PdfExportViewBase(ReportExportViewBase):
    _page_margin_left_right = 25
    _page_margin_top_bottom = 35
    _line_height = 12
    _small_line_height = 6
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
            self._width, self._height = letter
            self._write_area_width = self._width - self._page_margin_left_right * 2.0
            self._write_area_height = self._height - self._page_margin_top_bottom * 2.0
        return

    def _init_page(self):
        self._canvas.setFont(self._font_family, self._font_size)
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
        text = self._normalize_text(text)
        self._canvas.drawString(self._translate_X(self._current_X), self._translate_Y(self._current_Y), text)
        self._current_X = self._current_X + self._get_text_width(text) + trail_spacing
        return

    def _write_text_fix_width(self, text, text_width):
        text = self._normalize_text(text)
        computed_text_width = self._get_text_width(text)
        cut_text = None
        if text_width > 0 and computed_text_width > text_width:
            text_char_count = len(text)
            substring_char_count = int(text_char_count* int(text_width)/int(computed_text_width)) - 2
            cut_text = text[substring_char_count:]
            text = text[:substring_char_count] + '-'
        self._canvas.drawString(self._translate_X(self._current_X), self._translate_Y(self._current_Y), text)
        self._current_X = self._current_X + text_width
        return cut_text

    def _start_new_line(self):
        self.__start_new_line_internal(self._line_height)

    def __start_new_line_internal(self, line_height):
        self._current_X = 0
        self._current_Y = self._current_Y + line_height
        if self._current_Y > self._write_area_height:
            self._start_new_page()
        return

    def _write_line_uniform_width(self, text_items, segment_length_fractions=None):
        if text_items is None or len(text_items) <= 0:
            return

        if (segment_length_fractions is not None \
            and len(segment_length_fractions) != len(text_items)):
            raise ValueError("size of segment_length_percents does not match number of text items")

        if self._current_X > 0:
            self._start_new_line()

        # Compute segment length
        num_items = len(text_items)
        segment_lengths = [self._write_area_width / num_items for x in range(num_items)]
        if segment_length_fractions:
            # apply the override segment lengths
            for i, segment_length in enumerate(segment_lengths):
                segment_lengths[i] = self._write_area_width * segment_length_fractions[i]

        cut_text_array = [None] * num_items
        have_cut_text = True
        while have_cut_text:
            have_cut_text = False
            for idx, text in enumerate(text_items):
                cut_text = self._write_text_fix_width(text, segment_lengths[idx])
                if cut_text:
                    have_cut_text = True
                    cut_text_array[idx] = cut_text
            # End this line and move to next
            self._start_new_line()
            text_items = cut_text_array

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

    def _write_block_uniform_width(self, text_items_block, segment_length_fractions=None):
        if text_items_block is None or len(text_items_block) <= 0:
            return

        if (segment_length_fractions is not None \
            and len(segment_length_fractions) != len(text_items_block)):
            raise ValueError("size of segment_length_percents does not match number of text columns")

        if self._current_X > 0:
            self._start_new_line()

        num_columns = len(text_items_block)
        max_num_rows = len(max(text_items_block, key=len))

        # text_items_block is a 2-level nested list
        # e.g. [['a', 'b'], ['c']]
        # Here rearrange the contents of the block so
        # it can be rendered the normal way of render lines
        # e.g. [['a', 'c'], ['b', '']]
        block = [['' for x in range(num_columns)] for y in range(max_num_rows)]
        for i, text_items_list in enumerate(text_items_block):
            for j, text_item in enumerate(text_items_list):
                block[j][i] = text_item

        for line in block:
            self._write_line_uniform_width(line, segment_length_fractions)

        return

    def _draw_line(self):
        if self._current_X > 0:
            self._start_new_line()

        # Draw the line through the middle (aka at half way of the height)
        # of the current text line
        self._canvas.line(
            self._translate_X(0), \
            self._translate_Y(self._current_Y - self._line_height / 2), \
            self._translate_X(self._write_area_width), \
            self._translate_Y(self._current_Y \
                - self._line_height / 2 \
                + self._line_thickness))

        self.__start_new_line_internal(self._small_line_height)

        return

    def _normalize_text(self, text):
        result = text
        if (text is None):
            result = ''
        return str(result)
