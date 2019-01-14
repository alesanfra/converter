from decimal import Decimal
from xml.etree import ElementTree

from tornado.web import HTTPError

NAMESPACES = {'ex': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}


class ConversionMap:
    def __init__(self, conversion_rates, logger):
        self._rates = conversion_rates
        self.logger = logger

    @classmethod
    def from_xml_string(cls, xml_string, logger):
        logger.debug('Parsing XML')

        root = ElementTree.fromstring(xml_string)
        parsed = {}

        for cube in root.findall('.//ex:Cube[@time]', namespaces=NAMESPACES):
            parsed[cube.attrib['time']] = {c.attrib['currency']: Decimal(c.attrib['rate']) for c in cube}

        return cls(parsed, logger)

    def get_rate(self, currency, date):
        if date not in self._rates:
            self.logger.error("Date not found")
            raise HTTPError(404, reason="Date not found")

        if currency == 'EUR':
            return 1

        if currency not in self._rates[date]:
            self.logger.error("Unknown currency %s", currency)
            raise HTTPError(404, reason="Currency {} not found".format(currency))

        return self._rates[date][currency]

    def convert(self, src_currency, dst_currency, amount, reference_date):
        src_rate = self.get_rate(src_currency, reference_date)
        dst_rate = self.get_rate(dst_currency, reference_date)
        return float(round((amount / src_rate) * dst_rate, 2))
