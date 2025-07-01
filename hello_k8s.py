from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from datetime import datetime

@dag(
    dag_id="hello_world_simple",
    schedule=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["example"],
)
def hello_world_simple():
    BashOperator(
        task_id="say_hello",
        bash_command="echo 'Hello from Airflow!'",
    )

dag = hello_world_simple()
