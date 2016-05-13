from datetime import date
from django.test import TestCase
from app.service.date_time_service import DateTimeService


# Create your tests here.
class TestDateTimeService(TestCase):

    def test_get_list_of_week_start_dates_in_range__one_week(self):
        service = DateTimeService()

        start_date = date(2016, 5, 8)
        end_date = date(2016, 5, 8)

        result = service.get_list_of_week_start_dates_in_range(start_date, end_date)

        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 1)

        self.assertEqual(result[0], date(2016, 5, 8))

    def test_get_list_of_week_start_dates_in_range__two_weeks_at_start(self):
        service = DateTimeService()

        start_date = date(2016, 5, 8)
        end_date = date(2016, 5, 15)

        result = service.get_list_of_week_start_dates_in_range(start_date, end_date)

        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 2)

        self.assertEqual(result[0], date(2016, 5, 8))
        self.assertEqual(result[1], date(2016, 5, 15))

    def test_get_list_of_week_start_dates_in_range__two_weeks_at_end(self):
        service = DateTimeService()

        start_date = date(2016, 5, 14)
        end_date = date(2016, 5, 21)

        result = service.get_list_of_week_start_dates_in_range(start_date, end_date)

        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 2)

        self.assertEqual(result[0], date(2016, 5, 8))
        self.assertEqual(result[1], date(2016, 5, 15))

    def test_get_list_of_week_start_dates_in_range__three_weeks_at_middel(self):
        service = DateTimeService()

        start_date = date(2016, 5, 10)
        end_date = date(2016, 5, 25)

        result = service.get_list_of_week_start_dates_in_range(start_date, end_date)

        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 3)

        self.assertEqual(result[0], date(2016, 5, 8))
        self.assertEqual(result[1], date(2016, 5, 15))
        self.assertEqual(result[2], date(2016, 5, 22))
