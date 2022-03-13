import os, json
import boto3
from pydantic import ValidationError
from BaseModel import base_model
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')
index_name = os.environ.get('INDEX_NAME')
table = dynamodb.Table(table_name)

def list_post_by_user(sk):
    table_response = table.query(
        TableName = table_name,
        IndexName = index_name,
        ExpressionAttributeValues={
            ':sk': sk,
            },
        KeyConditionExpression='SK = :sk'
    )
    print(table_response)
    return table_response

def lambda_handler(event, context):
    print(event)
    body = json.loads(event['body'])
    sk = body['sk']
    try:
        response = list_post_by_user(sk)
        print(response)
        items = response['Items']
        print(items)
        return{
            'statusCode': 200,
            'body': json.dumps({
                'message': 'List of all Items',
                "list": items
            })
        }
    except ValidationError as e:
        return{
            'statusCode': 400,
            'body': json.dumps({
                'message': str(e)
            })
        }