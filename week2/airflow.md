# Airflow

## Installation
```
cd DE-Zoomcamp/week2/data-engineering-zoomcamp/cohorts/2022/week_2_data_ingestion/airflow
echo -e "AIRFLOW_UID=$(id -u)" > .env
docker-compose build
# change docker-compose.yaml (delete flower, celery, redis, etc)
docker-compose down --volumes --rmi all
docker-compose up airflow-init
docker-compose up
```
## Settings
1) open localhost:8080 in web browser
2) airflow;airflow with docker ps execute CONTAINER ID of scheduler
```
docker exec -it 7c6178fa5258 bash
ls
```
3) Can see the downloaded csv/parquet files there
4) if already have storage, bigquery dataset, parquet file should be uploaded to GCS.

# New!: Full Ingesting
1) make new folder and file dags_new/data_ingestion_local.py
2) write full code from scracth, test it with localhost:8080
3) to run, see code in Installation above from 'docker-compose build'
4) to check output file csv in docker process temp dir
```
docker exec -it $(container id of airflow_airflow-scheduler) bash
ls                                                            # at /opt/airflow
more output.csv
wc -l output.csv
```
5) to rerun in DAG, click first square, task action, clear

## put ingestion script into airflow that runs in docker; Docker Operator
