# Airflow

## Installation
```
cd DE-Zoomcamp/week2/data-engineering-zoomcamp/cohorts/2022/week_2_data_ingestion/airflow
echo -e "AIRFLOW_UID=$(id -u)" > .env
# START FROM THIS!
docker-compose build
# change docker-compose.yaml (delete flower, celery, redis, etc)
docker-compose down --volumes --rmi all
docker-compose up airflow-init
docker-compose up
```
## Run and ingest to GCS and BigQuery
1) open localhost:8080 in web browser
2) airflow;airflow with docker ps execute CONTAINER ID of scheduler
```
docker exec -it 7c6178fa5258 bash
ls
```
3) Can see the downloaded csv/parquet files there
4) if already have storage, bigquery dataset, parquet file should be uploaded to GCS.




# New!: Full Ingesting to local postgre
## getting started
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
1) make a new py script to ingest, add new req (pandas, etc) to Dockerfile
2) end all process, change earlier data_ingestion_local.py accordingly
3) specify pg params (host, user, etc) in .env, docker-compose.yaml, data_ingestion_local.py
4) integrating 2 docker-compose from the one from week1 using network
```
docker network ls
docker-compose build
docker-compose down --volumes --rmi all
docker-compose up
```
5) move to week1 docker-compose directory
```
docker-compose up
/home/usr/.local/bin/pgcli -h localhost -p 5432 -U root -d ny_taxi
\dt #empty database
docker ps
docker exec -it ${workflow_scheduler/worker} bash
python
```
```
from sqlalchemy  import create_engine
engine = create_engine('postgresql://root:root@pgdatabase:5432/ny_taxi')
engine.connect() #connect!
```
6) go to localhost:8080, rerun if it works
7) after ingestin data to table pgcli from ingesting_script.py, open pgcli
```
/home/usr/.local/bin/pgcli -h localhost -p 5432 -U root -d ny_taxi
\dt
SELECT count(1) FROM "yellow_tripdata_2021-01"; #should be not empty!
```
