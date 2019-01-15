# Currency converter
The **currency converter** application provides a web API endpoint to perform online currency conversion, based on the official rates published by the ECB.

## API

Base endpoint
> http://localhost:8000/api/v1/currency/convert

Parameters:
- **from**: source currency (e.g. USD)
- **to**: destination currency (e.g. CHF)
- **date**: reference date for the exchange rate (e.g. 2019-01-14)
- **amount**: amount to convert (e.g. 42.42) (optional, default 1)

Example:
> curl 'http://localhost:8000/api/v1/currency/convert?from=USD&to=CHF&amount=42.42&date=2019-01-14'


## Using Currency Converter

Requirements:
- Python 3.7+
- Pipenv installed on the machine (https://pipenv.readthedocs.io/en/latest/)

To install pipenv using pip

> pip install pipenv

### Install

> pipenv install --dev

### Run
To run the **Currency Converter** as a process first enter the virtualenv
> pipenv shell

Run the process
> PYTHONPATH=$PYTHONPATH:./src python bin/main.py



### Run in a docker container

Build the docker image
> docker build . -t currency_converter:latest

Run a container exposing port 8000
> docker run -p 8000:8000 currency_converter:latest

### Run unit tests
Enter the virtualenv
> pipenv shell

Run test with **pytest**
> PYTHONPATH=./src pytest test/unit/



### Run integration tests

Enter the virtualenv
> pipenv shell

Run integration tests with **robot framework**
> PYTHONPATH=./test/integration robot --outputdir out test/integration/





