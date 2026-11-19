import unittest
from datetime import datetime
from unittest.mock import patch

from inputs import get_symbol, get_chart_type, get_time_series, _get_date


class TestInputs(unittest.TestCase):

    def test_symbol(self):
        with patch("builtins.input", return_value="AAPL"):
            self.assertEqual(get_symbol(), "AAPL")

    def test_chart_type(self):
        with patch("builtins.input", return_value="1"):
            self.assertEqual(get_chart_type(), "Bar")

    def test_time_series(self):
        with patch("builtins.input", return_value="2"):
            self.assertEqual(
                get_time_series(),
                ("TIME_SERIES_DAILY", "Daily")
            )

    def test_start_date(self):
        with patch("builtins.input", return_value="2026-01-01"):
            self.assertEqual(
                _get_date("Start date: "),
                datetime(2026, 1, 1).date()
            )

    def test_end_date(self):
        with patch("builtins.input", return_value="2026-12-31"):
            self.assertEqual(
                _get_date("End date: "),
                datetime(2026, 12, 31).date()
            )
    def test_invalid_symbol(self):
        with patch("builtins.input", side_effect=["123", "TOOLONGSYMBOL", "AAPL"]):
            self.assertEqual(get_symbol(), "AAPL")

    def test_invalid_chart_type(self):
        with patch("builtins.input", side_effect=["3", "2"]):
            self.assertEqual(get_chart_type(), "Line")

    def test_invalid_time_series(self):
        with patch("builtins.input", side_effect=["5", "1"]):
            self.assertEqual(
                get_time_series(),
                ("TIME_SERIES_INTRADAY", "Intraday (60 min)")
            )

    def test_invalid_start_date(self):
        with patch("builtins.input", side_effect=["2026-13-01", "2026-01-01"]):
            self.assertEqual(
                _get_date("Start date: "),
                datetime(2026, 1, 1).date()
            )

    def test_invalid_end_date(self):
        with patch("builtins.input", side_effect=["2026-02-30", "2026-12-31"]):
            self.assertEqual(
                _get_date("End date: "),
                datetime(2026, 12, 31).date()
            )


if __name__ == "__main__":
    unittest.main()
