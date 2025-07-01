from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

with DAG(
    dag_id="hello_k8s",
    schedule=None,  # вместо schedule_interval=None
    start_date=datetime(2025, 6, 30),  # фиксированная дата, не datetime.now()
    catchup=False,
) as dag:

    hello_task = KubernetesPodOperator(
        task_id="hello_k8s_task",
        name="hello-task",
        namespace="airflow",
        image="busybox",
        cmds=["echo", "Hello from Kubernetes!"],
        is_delete_operator_pod=True,
    )
