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
