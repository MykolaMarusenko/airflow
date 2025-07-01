from airflow import DAG
from airflow.operators.python import PythonOperator
from kubernetes import client, config
from datetime import datetime

def create_configmap():
    config.load_incluster_config() 

    v1 = client.CoreV1Api()

    configmap = client.V1ConfigMap(
        metadata=client.V1ObjectMeta(name="test"),
        data={"message": "This is a test configmap created by Airflow."}
    )

    namespace = "airflow"
    v1.create_namespaced_config_map(namespace=namespace, body=configmap)

with DAG(
    dag_id="create_configmap_test",
    start_date=datetime(2023, 1, 1),
    schedule_interval="0 * * * *",
    catchup=False,
    tags=["k8s", "configmap"],
) as dag:

    create_task = PythonOperator(
        task_id="create_test_configmap",
        python_callable=create_configmap,
    )
