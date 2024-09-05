from airflow import DAG # type: ignore
from airflow.operators.python import PythonOperator # type: ignore
from datetime import datetime
from airflow.providers.amazon.aws.hooks.s3 import S3Hook # type: ignore
import pandas as pd # type: ignore
from datetime import datetime

def read_csv_from_s3(bucket_name, key):
    s3_hook = S3Hook(aws_conn_id='aws_default')
    # Download file to a temporary location
    file_obj = s3_hook.get_key(key, bucket_name).get()
    # Read the CSV content
    df = pd.read_csv(file_obj['Body'])
    print(df.head())  # Print the first few rows of the CSV file

# Define the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

with DAG(
    dag_id='read_s3_csv_dag',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
) as dag:

    read_csv_task = PythonOperator(
        task_id='read_csv_task',
        python_callable=read_csv_from_s3,
        op_args=['your-bucket-name', 'path/to/your-file.csv'],  # Replace with your bucket name and file path
    )

    read_csv_task

#bucket name -> airflow-dags-k8s
