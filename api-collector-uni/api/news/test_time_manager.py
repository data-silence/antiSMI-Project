import unittest
from datetime import datetime, timedelta
from freezegun import freeze_time
from time_manager import NewsTimeManager, ServiceMode


class TestNewsTimeManager(unittest.TestCase):
    def test_whole_mode_single_day(self):
        start_date = datetime(2023, 5, 1)
        manager = NewsTimeManager(ServiceMode.WHOLE, start_date)
        start, end = manager.get_time_range()

        self.assertEqual(start, datetime(2023, 5, 1))
        self.assertEqual(end, datetime(2023, 5, 1, 23, 59, 59))

    def test_whole_mode_date_range(self):
        start_date = datetime(2023, 5, 1)
        end_date = datetime(2023, 5, 3)
        manager = NewsTimeManager(ServiceMode.WHOLE, start_date, end_date)
        start, end = manager.get_time_range()

        self.assertEqual(start, datetime(2023, 5, 1))
        self.assertEqual(end, datetime(2023, 5, 3, 23, 59, 59))

    def test_whole_mode_no_start_date(self):
        manager = NewsTimeManager(ServiceMode.WHOLE)
        with self.assertRaises(ValueError):
            manager.get_time_range()

    @freeze_time("2023-05-01 15:00:00")
    def test_last24_mode(self):
        manager = NewsTimeManager(ServiceMode.LAST24)
        start, end = manager.get_time_range()

        expected_start = datetime(2023, 4, 30, 15, 0)
        expected_end = datetime(2023, 5, 1, 15, 0)
        self.assertEqual(start, expected_start)
        self.assertEqual(end, expected_end)

    @freeze_time("2023-05-01 00:30:00")
    def test_precision_mode_night(self):
        manager = NewsTimeManager(ServiceMode.PRECISION)
        start, end = manager.get_time_range()

        expected_start = datetime(2023, 4, 30, 21, 56)
        expected_end = datetime(2023, 5, 1, 0, 30)
        self.assertEqual(start, expected_start)
        self.assertEqual(end, expected_end)

    @freeze_time("2023-05-01 10:30:00")
    def test_precision_mode_morning(self):
        manager = NewsTimeManager(ServiceMode.PRECISION)
        start, end = manager.get_time_range()

        expected_start = datetime(2023, 4, 30, 21, 56)
        expected_end = datetime(2023, 5, 1, 10, 30)
        self.assertEqual(start, expected_start)
        self.assertEqual(end, expected_end)

    @freeze_time("2023-05-01 15:30:00")
    def test_precision_mode_afternoon(self):
        manager = NewsTimeManager(ServiceMode.PRECISION)
        start, end = manager.get_time_range()

        expected_start = datetime(2023, 5, 1, 8, 56)
        expected_end = datetime(2023, 5, 1, 15, 30)
        self.assertEqual(start, expected_start)
        self.assertEqual(end, expected_end)

    @freeze_time("2023-05-01 20:30:00")
    def test_precision_mode_evening(self):
        manager = NewsTimeManager(ServiceMode.PRECISION)
        start, end = manager.get_time_range()

        expected_start = datetime(2023, 5, 1, 12, 56)
        expected_end = datetime(2023, 5, 1, 20, 30)
        self.assertEqual(start, expected_start)
        self.assertEqual(end, expected_end)

    @freeze_time("2023-05-01 23:30:00")
    def test_precision_mode_late_night(self):
        manager = NewsTimeManager(ServiceMode.PRECISION)
        start, end = manager.get_time_range()

        expected_start = datetime(2023, 5, 1, 17, 56)
        expected_end = datetime(2023, 5, 1, 23, 30)
        self.assertEqual(start, expected_start)
        self.assertEqual(end, expected_end)

    @freeze_time("2023-05-01 03:30:00")
    def test_digest_mode_night(self):
        manager = NewsTimeManager(ServiceMode.DIGEST)
        start, end = manager.get_time_range()

        expected_start = datetime(2023, 4, 30, 17, 56)
        expected_end = datetime(2023, 4, 30, 21, 55, 59)
        self.assertEqual(start, expected_start)
        self.assertEqual(end, expected_end)

    @freeze_time("2023-05-01 10:30:00")
    def test_digest_mode_morning(self):
        manager = NewsTimeManager(ServiceMode.DIGEST)
        start, end = manager.get_time_range()

        expected_start = datetime(2023, 4, 30, 21, 56)
        expected_end = datetime(2023, 5, 1, 8, 55, 59)
        self.assertEqual(start, expected_start)
        self.assertEqual(end, expected_end)

    @freeze_time("2023-05-01 15:30:00")
    def test_digest_mode_afternoon(self):
        manager = NewsTimeManager(ServiceMode.DIGEST)
        start, end = manager.get_time_range()

        expected_start = datetime(2023, 5, 1, 8, 56)
        expected_end = datetime(2023, 5, 1, 12, 55, 59)
        self.assertEqual(start, expected_start)
        self.assertEqual(end, expected_end)

    @freeze_time("2023-05-01 20:30:00")
    def test_digest_mode_evening(self):
        manager = NewsTimeManager(ServiceMode.DIGEST)
        start, end = manager.get_time_range()

        expected_start = datetime(2023, 5, 1, 12, 56)
        expected_end = datetime(2023, 5, 1, 17, 55, 59)
        self.assertEqual(start, expected_start)
        self.assertEqual(end, expected_end)

    @freeze_time("2023-05-01 23:30:00")
    def test_digest_mode_late_night(self):
        manager = NewsTimeManager(ServiceMode.DIGEST)
        start, end = manager.get_time_range()

        expected_start = datetime(2023, 5, 1, 17, 56)
        expected_end = datetime(2023, 5, 1, 21, 55, 59)
        self.assertEqual(start, expected_start)
        self.assertEqual(end, expected_end)

    def test_unknown_mode(self):
        manager = NewsTimeManager("unknown_mode")
        with self.assertRaises(ValueError):
            manager.get_time_range()


if __name__ == '__main__':
    unittest.main()