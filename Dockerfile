FROM tiangolo/uwsgi-nginx-flask:python3.7

RUN mkdir -p /app
WORKDIR /app


RUN apt-get update && apt-get install -y \
    sqlite3 \
    postgresql-client libpq-dev \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*
RUN pip install pipenv
COPY ./Pipfile /app
COPY ./Pipfile.lock /app
RUN pipenv lock -r > requirements.txt && pip install -r requirements.txt
COPY . /app

# We must expose a port so Dokku lets us use it
ENV LISTEN_PORT 80
EXPOSE 80


ENV STATIC_PATH=/app/src/static
ENV FLASK_APP=/app/src

