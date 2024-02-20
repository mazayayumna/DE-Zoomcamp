FROM python:3.8-slim-buster

RUN /usr/local/bin/python -m pip install --upgrade pip --progress-bar off
RUN apt-get update && apt-get install -y libpq-dev build-essential
RUN apt-get install -y wget
RUN pip install psycopg2==2.9.9 --progress-bar off
RUN pip install pandas==2.0.3 --progress-bar off
RUN pip install sqlalchemy==2.0.27 --progress-bar off

WORKDIR /app
COPY ingest_data.py ingest_data.py

ENTRYPOINT ["python", "ingest_data.py"]