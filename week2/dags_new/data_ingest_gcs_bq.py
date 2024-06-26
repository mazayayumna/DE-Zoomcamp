# using dataset from github, csv instead of parquet, can be queried in bq
import os
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from google.cloud import storage
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator
import pyarrow.csv as pv
import pyarrow.parquet as pq

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")

dataset_file_zip = "yellow_tripdata_2021-01.csv.gz"
dataset_file = "yellow_tripdata_2021-01.csv"
dataset_file_wo_header = "yellow_tripdata_2021-01_woh.csv"
dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/{dataset_file_zip}"
path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", 'trips_data_all')


# NOTE: takes 20 mins, at an upload speed of 800kbps. Faster if your internet has a better upload speed
def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    :param bucket: GCS bucket name
    :param object_name: target path & file-name
    :param local_file: source path & file-name
    :return:
    """
    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    # End of Workaround

    client = storage.Client()
    bucket = client.bucket(bucket)

    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)


default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

# NOTE: DAG declaration - using a Context Manager (an implicit way)
with DAG(
    dag_id="data_ingestion_gcs_dag",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['dtc-de'],
) as dag:

    download_dataset_task = BashOperator(
        task_id="download_dataset_task",
        bash_command=f"curl -sSL {dataset_url} > {path_to_local_home}/{dataset_file_zip}"
    )

    unzip_dataset_task = BashOperator(
        task_id="unzip_dataset_task",
        bash_command=f"gzip -d {path_to_local_home}/{dataset_file_zip}"
    )

    rm_header_dataset_task = BashOperator(
        task_id="remove_csv_header",
        bash_command=f"tail -n +2 {path_to_local_home}/{dataset_file} > {path_to_local_home}/{dataset_file_wo_header}"
    )

    # TODO: Homework - research and try XCOM to communicate output values between 2 tasks/operators
    local_to_gcs_task = PythonOperator(
        task_id="local_to_gcs_task",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket": BUCKET,
            "object_name": f"raw/{dataset_file_wo_header}",
            "local_file": f"{path_to_local_home}/{dataset_file_wo_header}",
        },
    )

    bigquery_external_table_task = BigQueryCreateExternalTableOperator(
        task_id="bigquery_external_table_task",
        table_resource={
            "tableReference": {
                "projectId": PROJECT_ID,
                "datasetId": BIGQUERY_DATASET,
                "tableId": "trip_data_csv",
            },
            "externalDataConfiguration": {
                "sourceFormat": "CSV",
                "sourceUris": [f"gs://{BUCKET}/raw/{dataset_file_wo_header}"],
                # this option wont work to not read the header
                "options": {"skip_leading_rows": 1},
                "schema": {
                    "fields": [
		            {"name":"VendorID","type":"INTEGER"},
		            {"name":"tpep_pickup_datetime","type":"TIMESTAMP"},
		            {"name":"tpep_dropoff_datetime","type":"TIMESTAMP"},
		            {"name":"passenger_count","type":"INTEGER"},
		            {"name":"trip_distance","type":"FLOAT"},
		            {"name":"RatecodeID","type":"INTEGER"},
		            {"name":"store_and_fwd_flag","type":"BOOLEAN"},
		            {"name":"PULocationID","type":"INTEGER"},
		            {"name":"DOLocationID","type":"INTEGER"},
		            {"name":"payment_type","type":"INTEGER"},
		            {"name":"fare_amount","type":"FLOAT"},
		            {"name":"extra","type":"FLOAT"},
		            {"name":"mta_tax","type":"FLOAT"},
		            {"name":"tip_amount","type":"FLOAT"},
		            {"name":"tolls_amount","type":"FLOAT"},
		            {"name":"improvement_surcharge","type":"FLOAT"},
		            {"name":"total_amount","type":"FLOAT"},
		            {"name":"congestion_surcharge","type":"FLOAT"},
                    ]

                }
            },
        },
    )

    download_dataset_task >> unzip_dataset_task >> rm_header_dataset_task >> local_to_gcs_task >> bigquery_external_table_task
