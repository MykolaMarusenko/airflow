from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime

with DAG("master_dag", start_date=datetime(2023,1,1), schedule=None, catchup=False) as dag:

    trigger_a = TriggerDagRunOperator(
        task_id="trigger_dag_a",
        trigger_dag_id="dag_a",
    )
    wait_a = ExternalTaskSensor(
        task_id="wait_for_a",
        external_dag_id="dag_a",
        external_task_id=None,
        allowed_states=["success"],
        failed_states=["failed"],
        mode="poke",
        timeout=600,
        poke_interval=30,
    )

    trigger_b = TriggerDagRunOperator(
        task_id="trigger_dag_b",
        trigger_dag_id="dag_b",
    )
    wait_b = ExternalTaskSensor(
        task_id="wait_for_b",
        external_dag_id="dag_b",
        external_task_id=None,
        allowed_states=["success"],
        failed_states=["failed"],
        mode="poke",
        timeout=600,
        poke_interval=30,
    )

    trigger_c = TriggerDagRunOperator(
        task_id="trigger_dag_c",
        trigger_dag_id="dag_c",
    )
    wait_c = ExternalTaskSensor(
        task_id="wait_for_c",
        external_dag_id="dag_c",
        external_task_id=None,
        allowed_states=["success"],
        failed_states=["failed"],
        mode="poke",
        timeout=600,
        poke_interval=30,
    )

    trigger_a >> wait_a >> trigger_b >> wait_b >> trigger_c >> wait_c

    # После успешного завершения всех трёх DAG-ов — запускаем финальный DAG
    trigger_final = TriggerDagRunOperator(
        task_id="trigger_final_dag",
        trigger_dag_id="dag_final",
    )

    wait_c >> trigger_final
