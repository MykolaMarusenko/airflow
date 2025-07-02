from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def task_one():
    print("Running Task One")

def task_two():
    print("Running Task Two")

def task_three():
    print("Running Task Three")

with DAG(
    dag_id="multi_task_example",
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    t1 = PythonOperator(
        task_id="task_one",
        python_callable=task_one,
    )

    t2 = PythonOperator(
        task_id="task_two",
        python_callable=task_two,
    )

    t3 = PythonOperator(
        task_id="task_three",
        python_callable=task_three,
    )

    t1 >> [t2, t3] 
