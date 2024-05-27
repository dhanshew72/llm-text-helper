import boto3
import json


def get(name, region='us-west-2'):
    client = boto3.client('secretsmanager', region_name=region)
    get_secret_value_response = client.get_secret_value(SecretId=name)
    return json.loads(get_secret_value_response['SecretString'])
