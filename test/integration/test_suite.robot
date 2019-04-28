*** Settings ***
Documentation     A test suite for the convert currency app

Library          keywords
Library          DateTime


*** Test Cases ***
User can convert currency
    ${today}=                       Get Current Date     increment= -2 days    result_format=%Y-%m-%d
    set suite variable              ${today}
    ${result}=                      convert currency     USD     EUR       1        ${today}
    should be equal                 ${result['currency']}        EUR

User can convert to the same currency
    ${result}=                      convert currency     USD     USD       5        ${today}
    should be equal                 ${result['currency']}        USD
    should be equal as numbers      ${result['amount']}          5

User cannot convert from an unknown currency
    convert currency     XXX     USD       5        ${today}        expected_status_code=404

User cannot convert to an unknown currency
    convert currency     EUR     UUU       5        ${today}        expected_status_code=404

User cannot convert using a future date
    convert currency     EUR     UUU       5        2029-01-09      expected_status_code=404

User cannot convert using an invalid date
    convert currency     EUR     UUU       5        not-a-date      expected_status_code=400