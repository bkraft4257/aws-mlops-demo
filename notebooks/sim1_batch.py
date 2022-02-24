#
# https://raw.githubusercontent.com/aws-samples/sagemaker-ml-workflow-with-apache-airflow/master/src/dag_ml_pipeline_amazon_video_reviews.py
#

import sagemaker as sm

import os
from sim1_config import CONFIG


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

