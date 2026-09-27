#!/usr/bin/env bash
set -euo pipefail

if [ "${RUN_MIGRATIONS:-1}" = "1" ]; then
  echo "[entrypoint] waiting for the database..."
  python - <<'PY'
import sys, time
import django
django.setup()
from django.db import connection
deadline = time.time() + 90
while True:
    try:
        connection.ensure_connection()
        print("[entrypoint] database is up")
        break
    except Exception as exc:
        if time.time() > deadline:
            print(f"[entrypoint] database never became reachable: {exc}", file=sys.stderr)
            sys.exit(1)
        time.sleep(2)
PY
  echo "[entrypoint] running migrations"
  python manage.py migrate --noinput
fi

echo "[entrypoint] starting: $*"
exec "$@"
