from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

with DAG(
    dag_id="hello_k8s",
    schedule_interval=None,
    start_date=days_ago(1),
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
