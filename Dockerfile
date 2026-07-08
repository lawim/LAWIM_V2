# syntax=docker/dockerfile:1.7

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/code \
    LAWIM_HOST=0.0.0.0 \
    LAWIM_PORT=3000 \
    LAWIM_DB_PATH=/app/data/runtime/lawim.sqlite3 \
    LAWIM_SEED_DEMO_DATA=true \
    PATH="/app/code:${PATH}"

WORKDIR /app

RUN useradd --system --create-home --home-dir /home/lawim --shell /usr/sbin/nologin lawim \
    && mkdir -p /app/code /app/data/runtime \
    && chown -R lawim:lawim /app /home/lawim

COPY requirements.txt requirements-postgresql.txt /app/
COPY --chown=lawim:lawim sitecustomize.py /app/sitecustomize.py
COPY --chown=lawim:lawim code /app/code

RUN pip install --no-cache-dir -r /app/requirements.txt -r /app/requirements-postgresql.txt

USER lawim

EXPOSE 3000

CMD ["python", "-m", "lawim_v2"]
