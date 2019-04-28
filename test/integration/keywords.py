import json

import requests

DEFAULT_HEADERS = {"Content-Type": "application/json"}
BASE_URL = 'http://localhost:28027/api/v1/'


def convert_currency(src_currency=None, dst_currency=None, amount=None, reference_date=None, expected_status_code=200):
    paramters = {}
    if src_currency is not None:
        paramters['from'] = src_currency
    if dst_currency is not None:
        paramters['to'] = dst_currency
    if amount is not None:
        paramters['amount'] = amount
    if reference_date is not None:
        paramters['date'] = reference_date

    response = requests.get(BASE_URL + 'currency/convert', params=paramters, headers=DEFAULT_HEADERS)

    if response.status_code != int(expected_status_code):
        raise AssertionError("Expected response code {}, received {}".format(expected_status_code,
                                                                             response.status_code))
    if response.status_code < 300:
        return json.loads(response.content)

    return None
