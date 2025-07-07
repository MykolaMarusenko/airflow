from datetime import datetime
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator

with DAG(
    dag_id="hello_k8s",
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
    tags=["example"],
) as dag:

    hello_task = KubernetesPodOperator(
        task_id="hello_k8s_task",
        name="hello-task",
        namespace="airflow",
        image="busybox",
        cmds=["sh", "-c", "aws sts get-caller-identity"],
        is_delete_operator_pod=False,
        kubernetes_conn_id="mm-test",
        in_cluster=False,
        service_account_name="mm-airflow",
        namespace="krci-bff-mm-dev",
    )
