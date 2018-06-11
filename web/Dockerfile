FROM python:3.6.5

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/web

COPY . .

RUN pip install -r requirements/production.txt

EXPOSE 8000
