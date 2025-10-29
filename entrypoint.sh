#!/usr/bin/env bash
set -e

echo "🚀 Starting BrewNotes entrypoint..."

# Move to the app directory
cd /app

# Optional: wait for Postgres if needed
if [ -n "$DB_HOST" ]; then
  echo "⏳ Waiting for database at $DB_HOST..."
  while ! nc -z "$DB_HOST" "${DB_PORT:-5432}"; do
    sleep 1
  done
fi

echo "✅ Database reachable. Applying migrations and collecting static files..."

# Run migrations and collect static files
python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo "🏁 Launching Gunicorn server..."

# Start Gunicorn
exec gunicorn brewnotes.wsgi:application \
  --bind 0.0.0.0:${PORT:-8000} \
  --workers 3 \
  --timeout 60 \
  --access-logfile - \
  --error-logfile - \
  --forwarded-allow-ips="*"
