from datetime import datetime
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator

def my_task(**kwargs):
    param = kwargs.get('dag_run').conf.get('my_param', 'default_value')
    print(f"Parameter received: {param}")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 10, 8),
}

dag = DAG(
    dag_id='example_dag_with_config',
    default_args=default_args,
    schedule_interval=None,  # Set to None for manual triggering
    catchup=False,
)

start = DummyOperator(
    task_id='start',
    dag=dag,
)

run_task = PythonOperator(
    task_id='run_task',
    python_callable=my_task,
    provide_context=True,
    dag=dag,
)

start >> run_task
