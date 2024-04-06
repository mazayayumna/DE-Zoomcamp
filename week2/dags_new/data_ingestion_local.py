# my docker compose use lightweight airflow
import os
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow")

local_workflow = DAG(
    "LocalIngestionDag",
    schedule_interval="0 6 2 * *", # crontab-2nd day of the month 6AM
    start_date=datetime(2024, 1, 1)
)

url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

with local_workflow:
    wget_task = BashOperator(
        task_id = 'wget',
        bash_command = f'wget {url} -O {AIRFLOW_HOME}/output.csv.gz'
    )

    ingest_task = BashOperator(
        task_id = 'ingest',
        bash_command = f'ls {AIRFLOW_HOME}'
    )

    wget_task >> ingest_task