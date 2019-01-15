from decimal import Decimal
from unittest import TestCase
from unittest.mock import Mock, call

from tornado.web import HTTPError

from currency_converter.request.currency_handler import CurrencyConversionHandler


class TestCurrencyConversionHandler(TestCase):
    def setUp(self):
        self.mock_application = Mock(ui_methods={})
        self.mock_request = Mock(body=None)

        self.handler = CurrencyConversionHandler(application=self.mock_application,
                                                 request=self.mock_request)

        self.handler.get_argument = Mock()
        self.handler.write = Mock()

    def test_get(self):
        self.handler.get_argument.side_effect = ['FROM_CURR', 'TO_CURR', '2018-07-09', '10']

        self.handler.get()

        assert self.handler.get_argument.call_count == 4
        self.handler.get_argument.assert_has_calls([call('from'), call('to'), call('date'), call('amount', 1)])
        self.mock_application.rates.convert.assert_called_once_with('FROM_CURR', 'TO_CURR', Decimal('10'), '2018-07-09')
        self.handler.write.assert_called_once_with({
            'currency': 'TO_CURR',
            'amount': self.mock_application.rates.convert()
        })

    def test_get_invalid_date(self):
        self.handler.get_argument.side_effect = ['FROM_CURR', 'TO_CURR', 'not-a-date', '10']

        with self.assertRaises(HTTPError):
            self.handler.get()

        assert self.handler.get_argument.call_count == 4
        self.handler.get_argument.assert_has_calls([call('from'), call('to'), call('date'), call('amount', 1)])
        assert self.mock_application.rates.convert.call_count == 0
        assert self.handler.write.call_count == 0

    def test_get_invalid_amount(self):
        self.handler.get_argument.side_effect = ['FROM_CURR', 'TO_CURR', '2018-07-09', 'not-a-decimal']

        with self.assertRaises(HTTPError):
            self.handler.get()

        assert self.handler.get_argument.call_count == 4
        self.handler.get_argument.assert_has_calls([call('from'), call('to'), call('date'), call('amount', 1)])
        assert self.mock_application.rates.convert.call_count == 0
        assert self.handler.write.call_count == 0
