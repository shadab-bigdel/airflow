import os
import sys
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import logging

# Add the parent directory to the Python path to import the module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the external Python module
from my_module import process_data

# Function to call the external module and log the output
def task_with_logging():
    logging.info("Starting the task")
    
    # Call the function from the external module
    result = process_data()
    
    # Log the result
    logging.info(f"Result from process_data: {result}")
    logging.info("Task finished")

# Define the default_args for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 9, 1),
    'retries': 1,
}

# Create the DAG
with DAG(dag_id='import_python_module_dag',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:

    # Define the PythonOperator
    task1 = PythonOperator(
        task_id='log_info_task',
        python_callable=task_with_logging
    )

    task1
