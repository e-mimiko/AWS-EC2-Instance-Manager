# Author: Emiope Mimiko
# GitHub username: e-mimiko
# Date: 5/8/25
# Description: Test file for microservice server

from http.client import responses
import requests


def create_instance_body():
    body = {
        "ami_id": "ami-0c2b8ca1dad447f8a",#useast1 amazonlinux2023 free
        "instance_type": "t2.micro"#free tier
    }
    return body

def create_instance_client():
    url = "http://localhost:5670/create"
    headers = {"Content-Type": "application/json"}
    data = create_instance_body()
    print(data)
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        print("Success")
        print(response.json())
    else:
        print(f"Error: {response.reason}")


#test
create_instance_client()
