# from sagemaker import dataset_definition

# from airflow import AirflowException

# import boto3
# import os

# from airflow.providers.amazon.aws.operators.sagemaker
# from airflow.contrib.operators.sagemaker_training_operator import SageMakerTrainingOperator
# from airflow.contrib.operators.sagemaker_model_operator import SageMakerModelOperator
# from airflow.contrib.operators.sagemaker_endpoint_config_operator import SageMakerEndpointConfigOperator
# from airflow.contrib.operators.sagemaker_endpoint_operator import SageMakerEndpointOperator
# from airflow.operators.python_operator import BranchPythonOperator
# from airflow.contrib.hooks.aws_hook import AwsHook

# from sagemaker.processing import ScriptProcessor, ProcessingInput, ProcessingOutput
# from sagemaker.dataset_definition.inputs import RedshiftDatasetDefinition
# from sagemaker.dataset_definition import DatasetDefinition
# from sagemaker.network import NetworkConfig
# import sagemaker

#
# https://raw.githubusercontent.com/aws-samples/sagemaker-ml-workflow-with-apache-airflow/master/src/dag_ml_pipeline_amazon_video_reviews.py
#

from airflow import DAG
from airflow.utils.dates import days_ago
from datetime import timedelta

from airflow.operators.python import PythonOperator

import sagemaker as sm

import os


def batch_transform(in_config=None, input_filter=None):

    if in_config is None:
        in_config = CONFIG
   
    if input_filter is None:
        input_filter="$[1:]"

    # Retrieve Model    
    reg_model = sm.model.Model(image_uri=in_config['image_uri'], 
                               model_data=in_config['model_data'],
                               role=in_config['execution_role']
                               )

    # Build Transformer
    transformer = reg_model.transformer(
        instance_count=1,
        instance_type="ml.m4.xlarge",
        output_path=in_config['output_path'],
        assemble_with="Line",
        accept="text/csv",
       )

    # Predict With New Data
    transformer.transform(
        in_config['input_path'],
        content_type="text/csv",
        split_type="Line",
        input_filter=input_filter
    )


PROJECT = 'mlops-demo'
TAG = 'latest'

AWS_ACCOUNT_ID = 545053092614
IMAGE_URI = '382416733822.dkr.ecr.us-east-1.amazonaws.com/linear-learner:1'
REGION = 'us-east-1'

BUCKET ='bkraft-phdata' 
PROJECT='mlops-demo'
OUTPUT_PREFIX = f's3://{BUCKET}/{PROJECT}/sagemaker/simple-regression/sim_1/output'
PREDICT_PREFIX = f's3://{BUCKET}/{PROJECT}/sagemaker/simple-regression/sim_1/predict'

CONFIG = {
        'project': PROJECT,
        'bucket': BUCKET, 
        'region': REGION, 
        'image_uri': IMAGE_URI, 
        'model_data': f'{OUTPUT_PREFIX}/mlops-demo-20220223-20-17-24/output/model.tar.gz',
        'input_path': f'{PREDICT_PREFIX}/input', 
        'output_path': f'{PREDICT_PREFIX}/output', 
        'execution_role': 'arn:aws:iam::545053092614:role/service-role/AmazonSageMaker-ExecutionRole-20191104T123215',
    }

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
        python_callable=batch_transform
    )

    DataPreprocessing
