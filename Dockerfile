FROM python:3.12-slim-bullseye

COPY src src
COPY pyproject.toml src
WORKDIR src

ENV TZ=Europe/London
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update -y && \
        apt-get upgrade -y && \
        apt-get install -y gcc libxslt-dev libxml2-dev python3-dev lib32z1-dev
RUN pip3 install --upgrade pip && \
    pip install poetry
RUN poetry install

ENV LOGFILE /data/govuk_stats_log.json
