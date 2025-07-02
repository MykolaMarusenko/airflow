from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def task_a():
    print("Running Task A")

def task_b():
    print("Running Task B")

def task_c():
    print("Running Task C")

with DAG(
    dag_id="multi_task_example",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    t1 = PythonOperator(
        task_id="run_a",
        python_callable=task_a,
    )

    t2 = PythonOperator(
        task_id="run_b",
        python_callable=task_b,
    )

    t3 = PythonOperator(
        task_id="run_c",
        python_callable=task_c,
    )

    t1 >> [t2, t3]
