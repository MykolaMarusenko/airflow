from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="hello_world_simple",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    task = BashOperator(
        task_id="say_hello",
        bash_command="echo 'Hello from Airflow inside Kubernetes!'",
    )
