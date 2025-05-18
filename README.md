# AWS EC2 Instance Manager Microservice

## Description

This microservices manages the CRUD operation for the AWS EC2 Instances. You can add, remove, update and view AWS EC2 Instances using this microservice. 

## How to setup

Please download this repository to get started. This microservice is meant to run locally.

Included in this repository:  
**requirements.txt** \- these are the packages to install. Do this first.  
**server.py** \- this contains the microservice.

To get started with the Boto3 AWS SDK for Python, please follow the [installation guide](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html).  
An IAM User account is recommended for generating AWS credentials. Here is a good [tutorial](https://www.youtube.com/watch?v=ZQQe5En9oS8&ab_channel=CodeWithMuh) on this.

## How to request data

To request, use one of the various endpoints. To:

### Create an instance: POST /ec2-service/create

This will create and run a new EC2 Instance  
Request body (JSON):

| Attribute | Type | Required | Description | Example |
| :---- | :---- | :---- | :---- | :---- |
| `aws_access_key_id` | string | Yes | AWS account id | `-` |
| `aws_secret_access_key` | string | Yes | AWS account key | `-` |
| `region_name` | string | Yes | The region the instance should be created | `“us-east-1”` |
| `ami_id` | string | Yes | ID of the AMI to launch | `"ami-0c2b8ca1dad447f8"` |
| `instance_type` | string | Yes | EC2 instance type | `"t2.micro"` |
| `max_count` | integer | No | Maximum number of instances to launch | `1` |
| `min_count` | integer | No | Minimum number of instances to launch | `1` |
| `security_group_ids` | list\[string\] | No | List of security group IDs | `["sg-0d92db76742671f1e"]` |
| `subnet_id` | string | No | Subnet ID | `"subnet-09208976b53dbf945"` |

### Update an instance: PUT /ec2-service/update

This will update the instance type for EC2 Instance specified by `instance_id`. **Note**: This will stop and restart the Instance. 
Request body (JSON):

| Attribute | Type | Required | Description | Example |
| :---- | :---- | :---- | :---- | :---- |
| `aws_access_key_id` | string | Yes | AWS account id | `-` |
| `aws_secret_access_key` | string | Yes | AWS account key | `-` |
| `region_name` | string | Yes | The region associated with the EC2 Instance | `“us-east-1”` |
| `instance_id` | string | Yes | ID of the EC2 Instance | `"ami-0c2b8ca1dad447f8"` |
| `instance_type` | string | Yes | The EC2 Instance type to update the instance to | `"t3.micro"` |

### Delete an instance: PUT /ec2-service/delete

This will delete the EC2 Instance specified in `instance_id`  
Request body (JSON):

| Attribute | Type | Required | Description | Example |
| :---- | :---- | :---- | :---- | :---- |
| `aws_access_key_id` | string | Yes | AWS account id | `-` |
| `aws_secret_access_key` | string | Yes | AWS account key | `-` |
| `region_name` | string | Yes | The region associated with the EC2 Instance to be deleted | `“us-east-1”` |
| `instance_id` | string | Yes | ID of the EC2 Instance to terminate | `"ami-0c2b8ca1dad447f8"` |

### View all EC2 Instances: GET /ec2-service/view

This will return all EC2 Instances associated with the `region_name`.  
Request body (JSON):

| Attribute | Type | Required | Description | Example |
| :---- | :---- | :---- | :---- | :---- |
| `aws_access_key_id` | string | Yes | AWS account id | `-` |
| `aws_secret_access_key` | string | Yes | AWS account key | `-` |
| `region_name` | string | Yes | The region associated with the EC2 Instances | `“us-east-1”` |

### View an EC2 Instance: GET /ec2-service/viewById/<instance_id>

This will return the EC2 Instance specified by `instance_id`  
Path Parameter:

| Attribute | Type | Required | Description | Example |
| :---- | :---- | :---- | :---- | :---- |
| `instance_id` | string | Yes | ID of the EC2 Instance | `"ami-0c2b8ca1dad447f8"` |

Request body (JSON):

| Attribute | Type | Required | Description | Example |
| :---- | :---- | :---- | :---- | :---- |
| `aws_access_key_id` | string | Yes | AWS account id | `-` |
| `aws_secret_access_key` | string | Yes | AWS account key | `-` |
| `region_name` | string | Yes | The region associated with the EC2 Instance | `“us-east-1”` |

## How to receive data

A response will be sent back upon request. 

### GET Response (JSON)

| HTTP Status | Field          | Type   | Required | Description                      |
|-------------|----------------|--------|----------|----------------------------------|
| 200         | *\[ ]*         | list   | Yes      | List of EC2 Instance objects     |
|             | ─ `instance_id` | string | Yes      | The ID of the Instance           |
|             | ─ `state`       | string | Yes      | Current state of the Instance    |
|             | ─ `type`      | string | Yes      | Instance type (e.g., `t2.micro`) |

### DELETE/PUT/POST Response

| HTTP Status Code | Response Body Attribute | Required |
| :---- | :---- | :---- |
| 200 | \- | Yes |
| 400 | `reason` | Yes |
| 404 | `reason` | Yes |
| 500 | `reason` | Yes |
|  |  |  |

## Example call to request and receive data

To receive data from the microservice, a request must be placed. 

``` python  
    import requests
      
    url = "http://localhost:5670/ec2-service/view"
    headers = {"Content-Type": "application/json"}
    #call to get required attributes, and aws access credentials
    data = get_creds()
    #request to get instances
    response = requests.get(url, json=data, headers=headers)
    #response holds the response back from the microservice
    if response.status_code == 200:
        print("All Instances:\n", response.json())
    else:
        print(f"Error {response.status_code}: {response.reason}")
```

## UML Diagram
![Image](https://github.com/user-attachments/assets/c152641b-a359-493a-aef9-d02c5995208e)
