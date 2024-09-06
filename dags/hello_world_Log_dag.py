import logging
from airflow import DAG # type: ignore
from airflow.operators.python_operator import PythonOperator # type: ignore
from datetime import datetime

# Set up logging
logger = logging.getLogger("airflow.task")

def my_custom_function():
    logger.info("This is a custom log message from my DAG task.")
    print("This will also appear in the task logs.")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
}

with DAG('hello_world_Log_dag', default_args=default_args, schedule_interval='@daily') as dag:
    task = PythonOperator(
        task_id='hello_world_Log',
        python_callable=my_custom_function,
    )
