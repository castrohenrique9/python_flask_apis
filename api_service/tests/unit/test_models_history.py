# encoding: utf-8

import unittest
from api_service.models import History
from datetime import datetime as dt


class TestModelHistory(unittest.TestCase):

    date_now = None

    def setUp(self):
        self.date_now = dt.now()

    def test_when_init_new_user_then_ok(self):
        data = {
            "date": self.date_now,
            "name": "apple",
            "symbol": "appl.us",
            "open": 1.1,
            "high": 2.0,
            "low": 1.0,
            "close": 2.1,
            "user_id": 1,
        }
        history = History(data)

        assert history.date == self.date_now
        assert history.name == "apple"
        assert history.symbol == "appl.us"
        assert history.open == 1.1
        assert history.high == 2.0
        assert history.low == 1.0
        assert history.close == 2.1
        assert history.user_id == 1
