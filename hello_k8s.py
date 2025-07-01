from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

@dag(
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
    tags=["example"],
)
def hello_world_simple():
    say_hello = BashOperator(
        task_id="say_hello",
        bash_command="echo 'Hello from Airflow inside Kubernetes!'",
    )

    say_hello

dag_instance = hello_world_simple()
