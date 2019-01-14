from datetime import datetime
from decimal import Decimal

from tornado.web import RequestHandler, HTTPError


class CurrencyConversionHandler(RequestHandler):
    def get(self):
        src_currency, dest_currency, amount, reference_date = self._parse_arguments()

        if reference_date not in self.application.rates:
            self.application.logger.error("Date not found")
            raise HTTPError(404, reason="Date not found")

        src_rate = self.application.rates[reference_date].get(src_currency)
        dest_rate = self.application.rates[reference_date].get(dest_currency)

        reponse = {
            'currency': dest_currency,
            'amount': float(round((amount / src_rate) * dest_rate, 2))
        }
        self.write(reponse)

    def _parse_arguments(self):
        src_currency = self.get_argument("from")
        dest_currency = self.get_argument("to")
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
