import os
import json

import boto3
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/', methods=['GET'])
def upload_file():
    sts_connection = boto3.client('sts',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
        region_name='ap-northeast-1',
    )
    b = sts_connection.get_federation_token(
        Name="Bob",
        DurationSeconds=900,
        Policy='{"Version":"2012-10-17","Statement":[{"Sid":"Stmt1","Effect":"Allow","Action":"s3:PutObject","Resource":"*"}]}'
    )
    access_key_id = b['Credentials']['AccessKeyId']
    secret_access_key = b['Credentials']['SecretAccessKey']
    session_token = b['Credentials']['SessionToken']
    return render_template('index.html',
        access_key_id=access_key_id,
        secret_access_key=secret_access_key,
        session_token=session_token,
        bucket_name='your bucket name',
        object_key='your object key',
    )
