from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.hooks.S3_hook import S3Hook
from airflow.models import Variable
import logging
from airflow.operators.python_operator import PythonOperator

# Define the function to read from S3
def read_s3_file(**kwargs):
    try:
        # Fetching S3 bucket details from Airflow Variables
        s3_bucket = Variable.get('s3_bucket_name')
        s3_folder = Variable.get('s3_input_directory')
        s3_filename = Variable.get('s3_input_file')

        # Log the S3 details
        logging.info(f"Attempting to access S3 bucket: {s3_bucket}, folder: {s3_folder}, file: {s3_filename}")

        # Initialize the S3 Hook
        s3_hook = S3Hook(aws_conn_id='aws_default')  # Replace with your connection if needed

        # Build the key (folder + filename)
        s3_key = f"{s3_folder}/{s3_filename}"

        # Read the file from S3
        file_content = s3_hook.read_key(key=s3_key, bucket_name=s3_bucket)

        # Log file read success and content
        logging.info(f"Successfully accessed and read file from S3. Content: {file_content}")

    except Exception as e:
        logging.error(f"Error accessing or reading file from S3: {str(e)}")
        raise

# Define the DAG
with DAG(
    dag_id='s3_file_access_dag',
    default_args={
        'owner': 'airflow',
        'retries': 1,
    },
    description='A DAG to read file from S3 and log info or errors',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False
) as dag:

    # Define the PythonOperator to read the S3 file
    read_s3_task = PythonOperator(
        task_id='read_s3_file',
        python_callable=read_s3_file,
        provide_context=True
    )

    # Set the task sequence
    read_s3_task
