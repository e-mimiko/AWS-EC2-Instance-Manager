# Author: Emiope Mimiko
# GitHub username: e-mimiko
# Date: 5/8/25
# Description: Test file for microservice server

from http.client import responses
import requests

#Initializes a dictionary with the credentials to be passed
def get_creds():
    body = {
        "aws_access_key_id" : "AKIARDDIUQYBFK75BFDJ",
        "aws_secret_access_key" : "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",
        "region_name" : "us-east-1"
    }
    return body

#Sends a request to the microservice to create an instance
def create_instance():
    url = "http://localhost:5670/ec2-service/create"
    headers = {"Content-Type": "application/json"}
    data = get_creds()
    #other required fields for create
    data["ami_id"] = "ami-0c2b8ca1dad447f8a"
    data["instance_type"] = "t2.micro"
    #request
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        print(f"Status {response.status_code}: Successfully created Instance")
    else:
        print(f"Error: {response.reason}")


def delete_instance(id_to_delete):
    url = "http://localhost:5670/ec2-service/delete"
    headers = {"Content-Type": "application/json"}
    data = get_creds()
    data["instance_id"] = id_to_delete
    response = requests.delete(url, json=data, headers=headers)

    if response.status_code == 200:
        print("Instance Deleted Successfully")
    else:
        print(f"Error {response.status_code}: {response.reason}")

def get_all_instances():
    url = "http://localhost:5670/ec2-service/view"
    headers = {"Content-Type": "application/json"}
    data = get_creds()
    response = requests.get(url, json=data, headers=headers)
    if response.status_code == 200:
        print("All Instances:\n", response.json())
    else:
        print(f"Error {response.status_code}: {response.reason}")

def get_instance_by_id(instance_id):
    url = f"http://localhost:5670/ec2-service/viewById/{instance_id}"
    headers = {"Content-Type": "application/json"}
    data = get_creds()
    response = requests.get(url, json=data, headers=headers)
    if response.status_code == 200:
        print("Instance Requested:\n", response.json())
    else:
        print(f"Error {response.status_code}: {response.reason}")

#This function will temporarily stop the instance to change its type. It will be restarted right after.
def update_instance(instance_id, instance_type):
    url = f"http://localhost:5670/ec2-service/update"
    headers = {"Content-Type": "application/json"}
    data = get_creds()
    data["instance_id"] = instance_id
    data["instance_type"] = instance_type
    response = requests.put(url, json=data, headers=headers)
    if response.status_code == 200:
        print("Update successful")
    else:
        print(f"Error {response.status_code}: {response.reason}")


#test calls

#--create an instance
#create_instance()
#--create another instance
#create_instance()
#--get_all_instances
#get_all_instances()
#--get instance by id
#get_instance_by_id("i-06fbf84052ec35770")
#--update an instance by id
#update_instance("i-06fbf84052ec35770", "t3.micro")
#--get instance by id to show change in type
get_instance_by_id("i-06fbf84052ec35770")
