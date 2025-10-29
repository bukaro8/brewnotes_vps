#!/usr/bin/env bash
set -e

# Optional: wait for Postgres if needed
if [ -n "$POSTGRES_HOST" ]; then
  echo "Waiting for Postgres at $POSTGRES_HOST:$POSTGRES_PORT..."
  for i in {1..30}; do
    if pg_isready -h "$POSTGRES_HOST" -p "${POSTGRES_PORT:-5432}" -U "$POSTGRES_USER" >/dev/null 2>&1; then
      echo "Postgres is ready."
      break
    fi
    sleep 1
  done
fi

python manage.py migrate --noinput
# You’re on Cloudinary, but collectstatic is harmless and useful for admin
python manage.py collectstatic --noinput

# 👉 Replace 'projectname.wsgi' with your real module (folder containing wsgi.py)
exec gunicorn projectname.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3
