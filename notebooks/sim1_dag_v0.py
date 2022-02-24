from sagemaker import dataset_definition

from airflow import DAG
from airflow import AirflowException
from airflow.utils.dates import days_ago
from datetime import timedelta
import boto3
import os
from airflow.contrib.operators.sagemaker_training_operator import SageMakerTrainingOperator
from airflow.contrib.operators.sagemaker_model_operator import SageMakerModelOperator
from airflow.contrib.operators.sagemaker_endpoint_config_operator import SageMakerEndpointConfigOperator
from airflow.contrib.operators.sagemaker_endpoint_operator import SageMakerEndpointOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.contrib.hooks.aws_hook import AwsHook

from sagemaker.processing import ScriptProcessor, ProcessingInput, ProcessingOutput
from sagemaker.dataset_definition.inputs import RedshiftDatasetDefinition
from sagemaker.dataset_definition import DatasetDefinition
from sagemaker.network import NetworkConfig
import sagemaker

import sagemaker as sm


from sim1_batch import batch_transform

DEFAULT_ARGS = {
    'owner': 'Airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['bkraft@phdata.io'],
    'email_on_success': True,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0
}


with DAG(
    dag_id='mlops-demo-sim-1',
    default_args=DEFAULT_ARGS,
    dagrun_timeout=timedelta(hours=2),
    schedule_interval=None
) as dag:

    execution_date = '{{ ts_nodash }}'

    DataPreprocessing = PythonOperator(
        task_id='mlops-demo-sim-1-batch',
        provide_context=True,
        python_callable=batch_transform
    )

    DataPreprocessing
