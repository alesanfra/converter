from datetime import datetime
from decimal import Decimal

from tornado.web import RequestHandler, HTTPError


class CurrencyConversionHandler(RequestHandler):
    def get(self):
        src_currency, dest_currency, amount, reference_date = self._parse_arguments()
        converted_amount = self.application.rates.convert(src_currency, dest_currency, amount, reference_date)
        reponse = {
            'currency': dest_currency,
            'amount': converted_amount
        }
        self.write(reponse)

    def _parse_arguments(self):
        src_currency = self.get_argument("from").upper()
        dest_currency = self.get_argument("to").upper()
        reference_date = self.get_argument("date")
        amount = self.get_argument("amount", 1)

        try:
            amount = Decimal(amount)
        except (TypeError, ArithmeticError) as e:
            self.application.logger.error(e)
            raise HTTPError(400, reason="Invalid amount")

        try:
            reference_date = datetime.strptime(reference_date, "%Y-%m-%d").date().strftime("%Y-%m-%d")
        except ValueError as e:
            self.application.logger.error(e)
            raise HTTPError(400, reason="Invalid date")

        return src_currency, dest_currency, amount, reference_date
