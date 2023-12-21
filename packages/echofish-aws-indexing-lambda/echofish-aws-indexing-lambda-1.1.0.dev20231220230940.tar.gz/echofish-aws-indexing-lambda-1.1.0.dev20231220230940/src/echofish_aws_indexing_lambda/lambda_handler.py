#!/usr/bin/env python
"""
Bucket: https://ncei-wcsd-archive.s3.amazonaws.com/index.html
Duration 578579.80 ms --> 9.6 minutes
Max Memory Used: 3345 MB
Memory: 5000 MB, Storage: 1000 MB, Timeout 15 Minutes
Note: Requires Layer:
    AWSSDKPandas-Python39-Arm64, version 4, python3.9, arm64, arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python39-Arm64:4

(1) Run this to install needed files for arm. Note target folder:
    pip install --platform manylinux2014_armv7l --target=my-lambda-function-arm64 --implementation cp --python 3.9 --only-binary=:all: --upgrade botocore fsspec s3fs
(2) zip -r ../my-deployment-package-64.zip .
(3) aws --profile echofish s3 cp my-deployment-package-64.zip s3://noaa-wcsd-pds-index/
(4) create lambda

This file uses the calibration data found from https://docs.google.com/spreadsheets/d/1GpR1pu0ERfWlxDsQSDP9eOm94hRD_asy/edit#gid=1728447211
and stored in the bucket at "https://noaa-wcsd-pds-index.s3.amazonaws.com/calibrated_crusies.csv"

When run locally, all boto3.Sessions will need to have a profile enabled.
To enable the default profile have export AWS_DEFAULT_PROFILE=echofish set in your bashrc
"""

import os
import json
from .lambda_executor import LambdaExecutor

index_ek60_table_name = os.environ.get('INDEX_EK60_TABLE_NAME')
input_bucket_name = os.environ.get('INPUT_BUCKET_NAME')
calibration_bucket = os.environ.get('CALIBRATION_BUCKET')
calibration_key = os.environ.get('CALIBRATION_KEY')

executor = LambdaExecutor(index_ek60_table_name, input_bucket_name, calibration_bucket, calibration_key)

def handler(sns_event, context):
    print("Event : " + str(sns_event))
    print("Context : " + str(context))
    for record in sns_event['Records']:
        message = json.loads(record['Sns']['Message'])
        print("Start Message : " + str(message))
        executor.execute(message)
        print("Done Message : " + str(message))
    print("Done Event : " + str(sns_event))
