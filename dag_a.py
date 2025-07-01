from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def task_a(**kwargs):
    print("A complete!")
    kwargs["ti"].xcom_push(key="result_a", value="result-from-a")

with DAG(
    dag_id="dag_a",
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    run_a = PythonOperator(
        task_id="run_a",
        python_callable=task_a,
    )
