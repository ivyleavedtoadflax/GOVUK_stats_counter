FROM python:3.12-slim-bullseye

COPY src src
COPY pyproject.toml .
COPY uv.lock .

ENV TZ=Europe/London
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update -y && \
        apt-get upgrade -y && \
        apt-get install -y gcc libxslt-dev libxml2-dev python3-dev lib32z1-dev \
        libfreetype6-dev libpng-dev pkg-config

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Install dependencies
RUN uv sync --frozen

ENV LOGFILE=/data/govuk_stats_log.json

# Set the default command
ENTRYPOINT ["uv", "run"]
CMD ["python", "src/get_count.py"]