from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def task_c(**kwargs):
    print("C complete!")
    kwargs["ti"].xcom_push(key="result_c", value="result-from-c")

with DAG(
    dag_id="dag_c",
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    run_a = PythonOperator(
        task_id="run_c",
        python_callable=task_c,
    )
