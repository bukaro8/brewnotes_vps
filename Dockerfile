FROM python:3.8
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/
RUN python -m pip install --upgrade pip
RUN apt-get update && apt-get install -y postgresql-client
RUN pip install --no-cache-dir -r /code/requirements.txt

# bring the app in
COPY . /code/

# 👇 ensure Python can import packages from /code (so 'notes' resolves)
ENV PYTHONPATH="/code"

# make sure the entrypoint is executable
RUN chmod +x /code/entrypoint.sh

# start via entrypoint (it will migrate, collectstatic, then gunicorn)
CMD ["/code/entrypoint.sh"]
