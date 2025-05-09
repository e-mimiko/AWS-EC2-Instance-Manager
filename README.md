To get started with the AWS SDK for Python, please follow the installation guide: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html

The official key-value for the AWS instances use CamelCase

Change your .env file and include your own config and call the function

For the region name, ask David if he need it changes always as I might have to configure it

run_instances:
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/run_instances.html

default for create for these two are:
security_group_ids": 
"subnet_id":


figure out how to pass id, key and region name in all requests

