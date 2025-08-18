FROM python:3.8
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/

RUN python -m pip install --upgrade pip
RUN apt-get update && apt-get install -y postgresql-client
RUN pip install --no-cache-dir -r /code/requirements.txt

COPY . /code/