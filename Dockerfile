# syntax=docker/dockerfile:1

# ---------- builder: deps + collected static ----------
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

COPY requirements.txt /tmp/requirements.txt
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install -r /tmp/requirements.txt

COPY . /src
WORKDIR /src
# Collect (hash + compress) static files here, then drop the source copies so
# the runtime image only carries staticfiles/ once.
RUN DJANGO_SECRET_KEY=build-only /opt/venv/bin/python manage.py collectstatic --noinput \
    && find /src -path /src/staticfiles -prune -o -type d -name static -prune -exec rm -rf {} + \
    && mkdir -p /src/media \
    && chmod +x /src/entrypoint.sh

# ---------- runtime ----------
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    DJANGO_SETTINGS_MODULE=Fgen_New.settings \
    MEDIA_ROOT=/app/media

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 10001 appuser

COPY --from=builder /opt/venv /opt/venv
COPY --from=builder --chown=appuser:appuser /src /app

WORKDIR /app
USER appuser
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
    CMD curl -fsS -H "Host: localhost" http://127.0.0.1:8000/healthz/ || exit 1

ENTRYPOINT ["/app/entrypoint.sh"]
# 2 workers x 2 threads fits the 1 GB t3.micro host.
CMD ["gunicorn", "Fgen_New.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "2", \
     "--threads", "2", \
     "--timeout", "60", \
     "--max-requests", "1000", \
     "--max-requests-jitter", "100", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
