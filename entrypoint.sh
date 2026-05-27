#!/usr/bin/env bash
set -e

echo "🚀 Starting BrewNotes entrypoint..."

# Always run from the app root
cd /app

echo "Database environment:"
echo "DB_NAME=${DB_NAME}"
echo "DB_USER=${DB_USER}"
echo "DB_HOST=${DB_HOST}"
echo "DB_PORT=${DB_PORT:-5432}"

# Wait for Postgres WITHOUT nc (uses /dev/tcp)
if [ -n "$DB_HOST" ]; then
  echo "⏳ Waiting for database at $DB_HOST:${DB_PORT:-5432}..."
  for i in {1..60}; do
    (exec 3<>/dev/tcp/"$DB_HOST"/"${DB_PORT:-5432}") >/dev/null 2>&1 && break
    sleep 1
  done
  echo "✅ Database TCP port reachable."
fi

echo "✅ Applying migrations and collecting static..."
python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo "🏁 Launching Gunicorn..."
exec gunicorn brewnotes.wsgi:application \
  --bind 0.0.0.0:${PORT:-8000} \
  --workers 3 \
  --timeout 60 \
  --access-logfile - \
  --error-logfile - \
  --forwarded-allow-ips="*"
