# dag_final.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime, timedelta

def final_logic(**kwargs):
    ti = kwargs["ti"]
    a = ti.xcom_pull(task_ids="run_a", dag_id="dag_a", key="result_a")
    b = ti.xcom_pull(task_ids="run_b", dag_id="dag_b", key="result_b")
    c = ti.xcom_pull(task_ids="run_c", dag_id="dag_c", key="result_c")
    print(f"Results collected: A={a}, B={b}, C={c}")

with DAG(
    dag_id="dag_final",
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False
) as dag:

    wait_a = ExternalTaskSensor(
        task_id="wait_for_a",
        external_dag_id="dag_a",
        external_task_id="run_a",
        mode="poke",
        timeout=600,
        allowed_states=["success"],
        failed_states=["failed"],
        execution_delta=timedelta(seconds=0)
    )

    wait_b = ExternalTaskSensor(
        task_id="wait_for_b",
        external_dag_id="dag_b",
        external_task_id="run_b",
        mode="poke",
        timeout=600,
        allowed_states=["success"],
        failed_states=["failed"],
        execution_delta=timedelta(seconds=0)
    )

    wait_c = ExternalTaskSensor(
        task_id="wait_for_c",
        external_dag_id="dag_c",
        external_task_id="run_c",
        mode="poke",
        timeout=600,
        allowed_states=["success"],
        failed_states=["failed"],
        execution_delta=timedelta(seconds=0)
    )

    final_task = PythonOperator(
        task_id="run_final_logic",
        python_callable=final_logic,
    )

    [wait_a, wait_b, wait_c] >> final_task
