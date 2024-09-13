from airflow import DAG # type: ignore
from airflow.operators.python_operator import PythonOperator # type: ignore
from datetime import datetime, timedelta
import logging
import boto3 # type: ignore

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 9, 13),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the task that will be executed
def sample_task(**kwargs):
    logging.info("This is an info log.")  # Info log example
    try:
        # Your task logic here
        # Simulate an error
        raise ValueError("An error occurred!")
    except Exception as e:
        logging.error(f"Error encountered: {str(e)}")  # Error log example
    # Manually upload a log file to S3 for testing
    s3 = boto3.client('s3')
    log_data = "Sample log data from Airflow task"
    s3.put_object(Bucket='log-modsps', Key='airflow-logs/sample-log.txt', Body=log_data)

# Define the DAG and set up the task execution flow
with DAG('sample_dag',
         default_args=default_args,
         description='A simple DAG for logging to S3',
         schedule_interval='@daily',
         catchup=False) as dag:

    # Define the task
    task = PythonOperator(
        task_id='sample_task',
        python_callable=sample_task,
        provide_context=True  # Ensures kwargs are passed
    )

    # You can add more tasks here and set dependencies as needed
    task  # This triggers task execution in Airflow

