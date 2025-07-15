
FROM python:3.8
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/

RUN python -m pip install --upgrade pip
RUN apt-get update && apt-get install -y postgresql-client
RUN python -m pip install -r requirements.txt gunicorn  # ← Add gunicorn here

COPY . /code/

# Create a non-root user and switch to it
RUN useradd -m appuser && chown -R appuser:appuser /code
USER appuser

# Default command (can be overridden in docker-compose.yml)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "brewnotes.wsgi:application"]