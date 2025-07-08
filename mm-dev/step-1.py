from datetime import datetime
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from kubernetes.client import V1Pod, V1ObjectMeta, V1PodSpec, V1Container, V1ResourceRequirements


with DAG(
    dag_id="step-1-with-cleanup-and-main-task",
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
    tags=["step-1", "cleanup", "main"],
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
        # resources={
        #     "request_memory": "2Gi",
        #     "request_cpu": "500m",
        #     "limit_memory": "4Gi",
        #     "limit_cpu": "2"
        # },
        annotations={
        "ad.datadoghq.com/batch-aggregator.logs": """[{
            "source": "java",
            "log_processing_rules": [{
                "type": "multi_line",
                "name": "log_start_with_date",
                "pattern" : "\\\\d{4}-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01])"
            }]
        }]"""
        }
    )

    data_migration = KubernetesPodOperator(
        task_id="main-task",
        name="main-task",
        image="bitnami/kubectl:latest",
        cmds=["sh", "-c"],
        arguments=["kubectl get svc"],
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
        # resources={
        #     "request_memory": "20Gi",
        #     "request_cpu": "2",
        #     "limit_memory": "20Gi",
        #     "limit_cpu": "10"
        # },
        annotations={
        "ad.datadoghq.com/batch-aggregator.logs": """[{
            "source": "java",
            "log_processing_rules": [{
                "type": "multi_line",
                "name": "log_start_with_date",
                "pattern" : "\\\\d{4}-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01])"
            }]
        }]"""
        }
    )

    app_a_cleanup >> data_migration
