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

session = boto3.Session(
    aws_access_key_id = os.getenv("aws_access_key_id"),
    aws_secret_access_key = os.getenv("aws_secret_access_key"),
)

@app.route("/create", methods=["POST"])
def createInstance():
    data = request.get_json()
    ec2 = session.client('ec2', region_name=data.get("region_name"))
    #if verify input(data) is of correct type. dict.get will handle defaults:
    try:
        response = ec2.run_instances(
            ImageId = data.get("ami_id"),
            InstanceType = data.get("instance_type"),
            MaxCount = data.get("max_count", 1),
            MinCount = data.get("min_count", 1)
        )
        return jsonify(response["Instances"]), 200
    except botocore.exceptions.ClientError as Error:
        return jsonify({
            "reason": Error.response["Error"]["Message"]
        }), Error.response["ResponseMetadata"]["HTTPStatusCode"]



if __name__ == '__main__':
    app.run(debug=True, port=5670)


# sts = session.client("sts")
# identity = sts.get_caller_identity()
# print("Caller Identity:", identity)
#
# try:
#     response = ec2.run_instances(
#         ImageId="ami-0c2b8ca1dad447f8a",  # replace with a valid AMI for your region
#         InstanceType="t2.micro",
#         MinCount=1,
#         MaxCount=1
#     )
#     print("Success:", response)
# except Exception as e:
#     print("Error:", e)
