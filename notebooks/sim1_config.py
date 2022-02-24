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
