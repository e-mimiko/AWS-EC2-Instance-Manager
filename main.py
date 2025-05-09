# Author: Emiope Mimiko
# GitHub username: e-mimiko
# Date: 5/8/25
# Description: Test file for microservice server

import requests
import os
from dotenv import load_dotenv
import boto3

client = boto3.client(
    'ec2',
    aws_access_key_id = os.getenv("aws_access_key_id"),
    aws_secret_access_key = os.getenv("aws_secret_access_key"),
    region_name = "us-east-1"
)

def create_instance_body():
    body = {

    }
    return body


def create_instance_client():
    url = "https://localhost:5500/create"
    headers = {"Content-Type": "application/json"}
    data = create_instance_body()

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        print("Success")
        print(response.json())
    else:
        print(f"Error: {response.reason}")



