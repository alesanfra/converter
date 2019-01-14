import logging

from tornado.httpclient import HTTPClient
from tornado.ioloop import IOLoop
from tornado.web import Application

from currency_converter.conversion_map import ConversionMap
from currency_converter.request.handler.currency import CurrencyConversionHandler

API_ENDPOINTS = [
    (r"/api/v1/currency/conversion", CurrencyConversionHandler),
]


class ConverterApplication(Application):
    def __init__(self):
        super().__init__(handlers=API_ENDPOINTS)
        self.logger = self._get_logger()
        self.rates = None

    @staticmethod
    def _get_logger():
        logger = logging.getLogger(__name__)
        logging.basicConfig(
            level=logging.INFO,
            format="[%(levelname)s %(asctime)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S")
        return logger

    def start(self):
        self.logger.info('+--------- Starting Currency Converter ---------+')
        try:
            self.rates = self._fetch_rates()
        except Exception as e:
            self.logger.error(e)
            self.logger.error("Cannot fetch rates, shutting down")
            return

        self.listen(8000)
        self.logger.info("Listening on port: 8000")
        IOLoop.current().start()

    def _fetch_rates(self):
        self.logger.info("Fetching rates from ECB")
        http_client = HTTPClient()
        try:
            response = http_client.fetch("https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml")
            self.logger.debug(response.body)
        finally:
            http_client.close()

        self.logger.info("New rates fetched successfully!")
        return ConversionMap.from_xml_string(response.body, self.logger)
