from datetime import datetime
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from kubernetes.client import models as k8s

with DAG(
    dag_id="step-1",
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
    tags=["step-1"],
) as dag:

    app_a_cleanup = KubernetesPodOperator(
        task_id="app-a-cleanup",
        name="app-a-cleanup",
        image="bitnami/kubectl:latest",
        cmds=["sh", "-c"],
        arguments=[
            """
            echo "Getting replicas number for app-a"
            tbaReplicas=$(kubectl get statefulset dev-es-default -o jsonpath='{.spec.replicas}')

            echo "Scaling in app-a statefulset"
            kubectl scale statefulset dev-es-default --replicas=3

            echo "Removing app-a PVCs"
            kubectl get pvc -l 'common.k8s.elastic.co/type=elasticsearch'

            echo "Restoring app statefulsets"
            kubectl scale statefulset dev-es-default --replicas=$tbaReplicas

            kubectl get svc
            """
        ],
        namespace="krci-bff-mm-dev",
        service_account_name="mm-airflow",
        kubernetes_conn_id="mm-test",
        in_cluster=False,
        is_delete_operator_pod=False,
        # affinity={
        #     "nodeAffinity": {
        #         "requiredDuringSchedulingIgnoredDuringExecution": {
        #             "nodeSelectorTerms": [
        #                 {
        #                     "matchExpressions": [
        #                         {
        #                             "key": "workload",
        #                             "operator": "In",
        #                             "values": ["history-s3up"]
        #                         }
        #                     ]
        #                 }
        #             ]
        #         }
        #     }
        # },
        # tolerations=[
        #     {
        #         "key": "workload",
        #         "operator": "Equal",
        #         "value": "history-s3up",
        #         "effect": "NoSchedule"
        #     }
        # ],
        container_resources=k8s.V1ResourceRequirements(
            requests={"cpu": "2", "memory": "20Gi"},
            limits={"cpu": "10", "memory": "20Gi"}
        )
    )
