FROM python:3.7-slim-stretch

LABEL maintainer="sanfratello.alessio@gmail.com"

RUN pip install pipenv

RUN mkdir /app

WORKDIR /app
ENV PYTHONPATH "${PYTHONPATH}:/app/src"

# -- Adding Pipfiles
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

# -- Install dependencies:
RUN pipenv install --deploy --system

# -- Install Application into container:
COPY bin bin
COPY src src
EXPOSE 8000

CMD python bin/main.py
