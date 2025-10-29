FROM python:3.8

ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# Workdir
WORKDIR /code

# Install system packages needed by psycopg2 and friends
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt /code/
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r /code/requirements.txt

# App code
COPY . /code/

# Ensure dirs exist (harmless if you use Cloudinary)
RUN mkdir -p /code/staticfiles /code/media

# Expose Django/Gunicorn port
EXPOSE 8000

# Entrypoint runs migrations, collectstatic, then Gunicorn
COPY entrypoint.sh /code/entrypoint.sh
RUN chmod +x /code/entrypoint.sh

CMD ["/code/entrypoint.sh"]
