# Use 3.11 for speed/security. If you must stay on 3.8, swap the tag.
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOME=/app \
    PYTHONPATH=/app

WORKDIR $APP_HOME

# System deps for psycopg2 and friends
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Ensure entrypoint is executable (if present)
RUN chmod +x entrypoint.sh || true

EXPOSE 8000

# Run migrations/static in entrypoint, then start Gunicorn there
CMD ["bash", "entrypoint.sh"]
