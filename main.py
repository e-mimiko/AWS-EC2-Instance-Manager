# Author: Emiope Mimiko
# GitHub username: e-mimiko
# Date: 5/8/25
# Description: Test file for microservice server

from http.client import responses
import requests


def create_instance_body():
    body = {
        "ami_id": "ami-0c2b8ca1dad447f8a",#useast1 amazonlinux2023 free
        "instance_type": "t2.micro",#free tier
        "aws_access_key_id" : "AKIARDDIUQYBFK75BFDJ",
        "aws_secret_access_key" : "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",
        "region_name" : "us-east-1"
    }
    return body

def create_instance_client():
    url = "http://localhost:5670/create"
    headers = {"Content-Type": "application/json"}
    data = create_instance_body()
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        print("Success")
        response_data = response.json()
        return response_data.get("instance_id")
    else:
        response_error = "Error: " + response.reason
        return response_error


def delete_instance_client(id_to_delete):
    url = "http://localhost:5670/delete"
    headers = {"Content-Type": "application/json"}
    data = create_instance_body()
    data["instance_id"] = id_to_delete
    response = requests.delete(url, json=data, headers=headers)

    if response.status_code == 200:
        print("Instance Deleted Successfully")
    else:
        print(f"Error {response.status_code}: {response.reason}")


#test
#create_new instance and print ID
instance_id = create_instance_client()
print(instance_id)
delete_instance_client(instance_id)
