[![Build Status](https://travis-ci.org/alesanfra/converter.svg?branch=master)](https://travis-ci.org/alesanfra/converter)

# Currency converter
The **currency converter** application provides a web API endpoint to perform online currency conversion, based on the official rates published by the ECB.

The latest rates are retrieved at the application startup from the following endpoint:
```
https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml
```

## API

Base endpoint
```
http://localhost:8000/api/v1/currency/convert
```

Parameters:
- **from**: source currency (e.g. USD)
- **to**: destination currency (e.g. CHF)
- **date**: reference date for the exchange rate (e.g. 2019-01-14)
- **amount**: amount to convert (e.g. 42.42) (optional, default 1)

Example:
```bash
curl 'http://localhost:8000/api/v1/currency/convert?from=USD&to=CHF&amount=42.42&date=2019-01-14'
```


## Using Currency Converter

Requirements:
- Python 3.7+
- Pipenv installed on the machine (https://pipenv.readthedocs.io/en/latest/)

To install pipenv using pip

```bash
pip install pipenv
```

### Install
```bash
pipenv install --dev
```

### Run
To run the **Currency Converter** as a process:
```bash
PYTHONPATH=$PYTHONPATH:./src pipenv run python bin/main.py
```

### Run in a docker container
Build the docker image
```bash
docker build . -t currency_converter:latest
```

Run a container exposing port 8000
```bash
docker run -p 8000:8000 currency_converter:latest
```

### Run unit tests
Run tests with **pytest**
```bash
PYTHONPATH=./src pipenv run pytest test/unit/
```

### Run integration tests
Run integration tests with **robot framework**
```bash
PYTHONPATH=./test/integration pipenv run robot --outputdir out test/integration/
```
