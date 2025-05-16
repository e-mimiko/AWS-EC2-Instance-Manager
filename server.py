# Author: Emiope Mimiko
# GitHub username: e-mimiko
# Date: 5/8/25
# Description: AWS EC2 Instance Manager
from flask import Flask, request, jsonify
import boto3
import botocore.exceptions



app = Flask(__name__)

def create_ec2_client(service, key_id, key, region):
    session = boto3.Session(
        aws_access_key_id = key_id,
        aws_secret_access_key = key,
        region_name = region
    )
    ec2 = session.client(service)
    return ec2

def create_ec2_resource(service, key_id, key, region):
    session = boto3.Session(
        aws_access_key_id = key_id,
        aws_secret_access_key = key,
        region_name = region
    )
    ec2 = session.resource(service)
    return ec2

@app.route("/ec2-service/create", methods=["POST"])
def createInstance():
    data = request.get_json()
    ec2 = create_ec2_client("ec2", data.get("aws_access_key_id",""),
            data.get("aws_secret_access_key",""),data.get("region_name", ""))
    parameters = {
        "ImageId" : data.get("ami_id"),
        "InstanceType" : data.get("instance_type"),
        "MaxCount" : data.get("max_count", 1),
        "MinCount" : data.get("min_count", 1)
    }
    if data.get("security_group_ids"):
        parameters["SecurityGroupIds"] = data.get("security_group_ids")
    if data.get("subnet_id"):
        parameters["SubnetId"] = data.get("subnet_id")
    try:
        ec2.run_instances(**parameters)
        return "", 200
    except botocore.exceptions.ClientError as Error:
        return jsonify({
            "reason": Error.response["Error"]["Message"]
        }), Error.response["ResponseMetadata"]["HTTPStatusCode"]

#terminate an instance
@app.route("/ec2-service/delete", methods=["DELETE"])
def deleteInstance():
    data = request.get_json()
    ec2 = create_ec2_client("ec2", data.get("aws_access_key_id",""),
            data.get("aws_secret_access_key",""),data.get("region_name", ""))
    try:
        ec2.terminate_instances(
            InstanceIds = [data.get("instance_id")],
        )
        return "", 200
    except botocore.exceptions.ClientError as Error:
        return jsonify({
            "reason": Error.response["Error"]["Message"]
        }), Error.response["ResponseMetadata"]["HTTPStatusCode"]

#view all instances
@app.route("/ec2-service/view", methods=["GET"])
def getAllInstances():
    creds = request.get_json()
    ec2 = create_ec2_resource("ec2", creds.get("aws_access_key_id",""),
            creds.get("aws_secret_access_key",""),creds.get("region_name", ""))
    return_data = []
    try:
        for instance in ec2.instances.all():
            instance_dict = {"instance_id": instance.id, "state":instance.state["Name"], "type": instance.instance_type}
            return_data.append(instance_dict)
        return jsonify(return_data), 200
    except botocore.exceptions.ClientError as Error:
        return jsonify({
            "reason": Error.response["Error"]["Message"]
        }), Error.response["ResponseMetadata"]["HTTPStatusCode"]

#view all instances
@app.route("/ec2-service/viewById/<instance_id>", methods=["GET"])
def getInstanceById(instance_id):
    creds = request.get_json()
    ec2 = create_ec2_resource("ec2", creds.get("aws_access_key_id",""),
            creds.get("aws_secret_access_key",""),creds.get("region_name", ""))
    try:
        instance = ec2.Instance(instance_id)
        instance_dict = {"instance_id": instance.id, "state": instance.state["Name"], "type": instance.instance_type}
        return jsonify(instance_dict), 200
    except botocore.exceptions.ClientError as Error:
        return jsonify({
            "reason": Error.response["Error"]["Message"]
        }), Error.response["ResponseMetadata"]["HTTPStatusCode"]

#update an instance
@app.route("/ec2-service/update", methods=["PUT"])
def updateInstance():
    data = request.get_json()
    ec2 = create_ec2_client("ec2", data.get("aws_access_key_id",""),
            data.get("aws_secret_access_key",""),data.get("region_name", ""))
    try:
        ec2.stop_instances(InstanceIds = [data.get("instance_id","")])
        ec2.get_waiter('instance_stopped').wait(InstanceIds=[data.get("instance_id","")])
        try:
            ec2.modify_instance_attribute(
                InstanceId = data.get("instance_id",""),
                InstanceType = {"Value": data.get("instance_type","")}
            )
            try:
                ec2.start_instances(InstanceIds=[data.get("instance_id", "")])
                return "", 200
            except botocore.exceptions.ClientError as Error:
                return jsonify({
                    "reason": Error.response["Error"]["Message"]
                }), Error.response["ResponseMetadata"]["HTTPStatusCode"]
        except botocore.exceptions.ClientError as Error:
            return jsonify({
                "reason": Error.response["Error"]["Message"]
            }), Error.response["ResponseMetadata"]["HTTPStatusCode"]
    except botocore.exceptions.ClientError as Error:
        return jsonify({
            "reason": Error.response["Error"]["Message"]
        }), Error.response["ResponseMetadata"]["HTTPStatusCode"]




if __name__ == '__main__':
    app.run(debug=True, port=5670)
