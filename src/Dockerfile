# Multibuild to minimize image size
FROM python:3.11-alpine AS builder

WORKDIR /app
COPY poetry.lock pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry==1.7.1 \
 && poetry config virtualenvs.in-project true \
 && poetry install --without dev --no-interaction --no-ansi --no-root


FROM python:3.11-alpine as base-app

WORKDIR /app

COPY --from=builder /app /app
COPY src /app/src

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV CONFIG_FILE=config.yaml

CMD /app/.venv/bin/python ./src/main.py $CONFIG_FILE
