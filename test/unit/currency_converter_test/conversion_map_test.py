from decimal import Decimal
from unittest import TestCase
from unittest.mock import Mock

from currency_converter.conversion_map import ConversionMap

FAKE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<gesmes:Envelope xmlns:gesmes="http://www.gesmes.org/xml/2002-08-01"
                 xmlns="http://www.ecb.int/vocabulary/2002-08-01/eurofxref">
    <gesmes:subject>Reference rates</gesmes:subject>
    <gesmes:Sender>
        <gesmes:name>European Central Bank</gesmes:name>
    </gesmes:Sender>
    <Cube>
        <Cube time="2019-01-08">
            <Cube currency="USD" rate="1.144"/>
            <Cube currency="JPY" rate="124.46"/>
            <Cube currency="BGN" rate="1.9558"/>
            <Cube currency="CZK" rate="25.642"/>
            <Cube currency="DKK" rate="7.4663"/>
            <Cube currency="GBP" rate="0.89743"/>
            <Cube currency="HUF" rate="322.15"/>
            <Cube currency="PLN" rate="4.3055"/>
            <Cube currency="RON" rate="4.671"/>
            <Cube currency="SEK" rate="10.1855"/>
            <Cube currency="CHF" rate="1.1232"/>
            <Cube currency="ISK" rate="136.1"/>
            <Cube currency="NOK" rate="9.775"/>
            <Cube currency="HRK" rate="7.4296"/>
            <Cube currency="RUB" rate="76.7197"/>
            <Cube currency="TRY" rate="6.2851"/>
            <Cube currency="AUD" rate="1.6042"/>
            <Cube currency="BRL" rate="4.2604"/>
            <Cube currency="CAD" rate="1.5208"/>
            <Cube currency="CNY" rate="7.8405"/>
            <Cube currency="HKD" rate="8.9671"/>
            <Cube currency="IDR" rate="16181.88"/>
            <Cube currency="ILS" rate="4.2312"/>
            <Cube currency="INR" rate="80.245"/>
            <Cube currency="KRW" rate="1288.62"/>
            <Cube currency="MXN" rate="22.1599"/>
            <Cube currency="MYR" rate="4.7053"/>
            <Cube currency="NZD" rate="1.7023"/>
            <Cube currency="PHP" rate="60.057"/>
            <Cube currency="SGD" rate="1.5549"/>
            <Cube currency="THB" rate="36.705"/>
            <Cube currency="ZAR" rate="16.0365"/>
        </Cube>
    </Cube>
</gesmes:Envelope>
"""


class TestConversionMap(TestCase):
    def setUp(self):
        self.mock_logger = Mock()

    def test_build_from_xml(self):
        rates = ConversionMap.from_xml_string(FAKE_XML, self.mock_logger)

        assert rates._rates == {
            '2019-01-08': {
                'AUD': Decimal('1.6042'),
                'BGN': Decimal('1.9558'),
                'BRL': Decimal('4.2604'),
                'CAD': Decimal('1.5208'),
                'CHF': Decimal('1.1232'),
                'CNY': Decimal('7.8405'),
                'CZK': Decimal('25.642'),
                'DKK': Decimal('7.4663'),
                'GBP': Decimal('0.89743'),
                'HKD': Decimal('8.9671'),
                'HRK': Decimal('7.4296'),
                'HUF': Decimal('322.15'),
                'IDR': Decimal('16181.88'),
                'ILS': Decimal('4.2312'),
                'INR': Decimal('80.245'),
                'ISK': Decimal('136.1'),
                'JPY': Decimal('124.46'),
                'KRW': Decimal('1288.62'),
                'MXN': Decimal('22.1599'),
                'MYR': Decimal('4.7053'),
                'NOK': Decimal('9.775'),
                'NZD': Decimal('1.7023'),
                'PHP': Decimal('60.057'),
                'PLN': Decimal('4.3055'),
                'RON': Decimal('4.671'),
                'RUB': Decimal('76.7197'),
                'SEK': Decimal('10.1855'),
                'SGD': Decimal('1.5549'),
                'THB': Decimal('36.705'),
                'TRY': Decimal('6.2851'),
                'USD': Decimal('1.144'),
                'ZAR': Decimal('16.0365')
            }}

    def test_conversion(self):
        rates = ConversionMap.from_xml_string(FAKE_XML, self.mock_logger)

        amount = rates.convert('EUR', 'AUD', Decimal(10), '2019-01-08')

        assert amount == 16.04
