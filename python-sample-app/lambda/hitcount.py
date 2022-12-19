import json
import os

import boto3

ddb = boto3.resource('dynamodb')
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html#using-an-existing-table
table = ddb.Table(os.environ['HITS_TABLE_NAME'])
_lambda = boto3.client('lambda')

def handler(event, context):
    print("request: ", json.dumps(event))

    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html#updating-an-item
    table.update_item(
        Key={"path": event["path"]},
        UpdateExpression="ADD hits :incr",
        ExpressionAttributeValues={":incr": 1}
    )

    resp = _lambda.invoke(
        FunctionName=os.environ["DOWNSTREAM_FUNCTION_NAME"],
        Payload=json.dumps(event)
    )

    body = resp['Payload'].read()

    print("downstream response: ", body)

    return json.loads(body)
