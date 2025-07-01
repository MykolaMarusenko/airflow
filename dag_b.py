from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def task_b(**kwargs):
    print("B complete!")
    kwargs["ti"].xcom_push(key="result_b", value="result-from-b")

with DAG(
    dag_id="dag_b",
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    run_a = PythonOperator(
        task_id="run_b",
        python_callable=task_b,
    )
