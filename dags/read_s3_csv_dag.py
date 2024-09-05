import logging
from airflow import DAG # type: ignore
from airflow.operators.python import PythonOperator # type: ignore
from datetime import datetime
from airflow.providers.amazon.aws.hooks.s3 import S3Hook # type: ignore
import pandas as pd # type: ignore
from datetime import datetime

# Set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_csv_from_s3(bucket_name, key):
    try:
        logger.info("Starting to connect to S3")
        s3_hook = S3Hook(aws_conn_id='aws_default')
        
        logger.info(f"Fetching file from S3 bucket: {bucket_name}, key: {key}")
        file_obj = s3_hook.get_key(key, bucket_name).get()
        
        logger.info("Reading CSV file into pandas DataFrame")
        df = pd.read_csv(file_obj['Body'])
        
        logger.info(f"CSV file read successfully. DataFrame head:\n{df.head()}")
        return df

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

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
        op_args=['airflow-dags-k8s', 'input/COMEXT_INTRA_M_NL_tiny.csv'],  # Replace with your bucket name and file path
    )

    read_csv_task

