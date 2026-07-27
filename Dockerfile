# syntax=docker/dockerfile:1.7

FROM python:3.12-slim

ARG LAWIM_BUILD_SHA=unknown

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/code:/app/lawim_runtime \
    LAWIM_HOST=0.0.0.0 \
    LAWIM_PORT=3000 \
    LAWIM_DB_PATH=/app/data/runtime/lawim.sqlite3 \
    LAWIM_SEED_DEMO_DATA=true \
    PATH="/app/code:${PATH}" \
    LAWIM_BUILD_SHA=${LAWIM_BUILD_SHA} \
    LAWIM_FEATURE_CONVERSATION_V2=true \
    PROGRAM_F_ENABLED=true

LABEL org.opencontainers.image.revision=${LAWIM_BUILD_SHA}

WORKDIR /app

RUN useradd --system --create-home --home-dir /home/lawim --shell /usr/sbin/nologin lawim \
    && mkdir -p /app/code /app/data/runtime /app/data/runtime/media /app/data/runtime/snapshots \
    && chown -R lawim:lawim /app /home/lawim

COPY requirements.txt requirements-postgresql.txt /app/
COPY --chown=lawim:lawim sitecustomize.py /app/sitecustomize.py
COPY --chown=lawim:lawim code /app/code
COPY --chown=lawim:lawim lawim_runtime /app/lawim_runtime
COPY --chown=lawim:lawim scripts/entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh \
    && pip install --no-cache-dir -r /app/requirements.txt -r /app/requirements-postgresql.txt \
    && echo "${LAWIM_BUILD_SHA}" > /app/BUILD_SHA

USER lawim

EXPOSE 3000

ENTRYPOINT ["/app/entrypoint.sh"]
