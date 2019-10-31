FROM python:3.6-slim-stretch

COPY src src
WORKDIR src

RUN apt-get update -y && apt-get upgrade -y
RUN pip3 install -r requirements.txt

ENV LOGFILE /data/govuk_stats_log.json

ENTRYPOINT ["python3"]
CMD "get_count.py"
