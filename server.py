# Author: Emiope Mimiko
# GitHub username: e-mimiko
# Date: 5/8/25
# Description: AWS EC2 Instance Manager
from crypt import methods

from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import boto3
import botocore.exceptions

load_dotenv()

app = Flask(__name__)

def create_ec2_client(service, key_id, key, region):
    session = boto3.Session(
        aws_access_key_id = key_id,
        aws_secret_access_key = key,
        region_name = region
    )
    ec2 = session.client(service)
    return ec2

@app.route("/create", methods=["POST"])
def createInstance():
    data = request.get_json()
    #if verify input(data) is of correct type. dict.get will handle defaults:
    ec2 = create_ec2_client("ec2", data.get("aws_access_key_id",""),
            data.get("aws_secret_access_key",""),data.get("region_name", ""))
    try:
        response = ec2.run_instances(
            ImageId = data.get("ami_id"),
            InstanceType = data.get("instance_type"),
            MaxCount = data.get("max_count", 1),
            MinCount = data.get("min_count", 1)
        )
        #get id, state and type
        new_instance_id = response["Instances"][0]["InstanceId"]
        new_instance_state = response["Instances"][0]["State"]
        new_instance_type = response["Instances"][0]["InstanceType"]
        #create new dictionary
        return_data = {"instance_id": new_instance_id, "state": new_instance_state, "type": new_instance_type}
        return jsonify(return_data), 200
    except botocore.exceptions.ClientError as Error:
        return jsonify({
            "reason": Error.response["Error"]["Message"]
        }), Error.response["ResponseMetadata"]["HTTPStatusCode"]

@app.route("/delete", methods=["DELETE"])
def deleteInstance():
    data = request.get_json()
    #if verify input(data) is of correct type. dict.get will handle defaults:
    ec2 = create_ec2_client("ec2", data.get("aws_access_key_id",""),
            data.get("aws_secret_access_key",""),data.get("region_name", ""))
    try:
        response = ec2.terminate_instances(
            InstanceIds = [data.get("instance_id")],
        )
        return "", 200
    except botocore.exceptions.ClientError as Error:
        return jsonify({
            "reason": Error.response["Error"]["Message"]
        }), Error.response["ResponseMetadata"]["HTTPStatusCode"]



if __name__ == '__main__':
    app.run(debug=True, port=5670)
