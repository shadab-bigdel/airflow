from airflow import DAG # type: ignore
from airflow.operators.python import PythonOperator # type: ignore
from datetime import datetime
import logging

# Define functions for tasks
def log_hello_message():
    logging.info("Hello log from DAG")

def log_goodbye_message():
    logging.info("Goodbye log from DAG")

# Define the DAG
with DAG(
    dag_id='manual_hello_log_dag',
    start_date=datetime(2023, 9, 8),
    schedule_interval=None,
    catchup=False,
    tags=['example'],
) as dag:
    
    # Define tasks
    log_hello_task = PythonOperator(
        task_id='log_hello_message',
        python_callable=log_hello_message,
    )

    log_goodbye_task = PythonOperator(
        task_id='log_goodbye_message',
        python_callable=log_goodbye_message,
    )

    # Set task dependencies
    log_hello_task >> log_goodbye_task