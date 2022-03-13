import json
import boto3
import os
from pydantic import ValidationError

# from boto3.dynamodb.conditions import Key, Attr
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')
table = dynamodb.Table(table_name)

def read_post(pk,sk):
    table_response = table.get_item(
        TableName = table_name,
        Key={
            'PK': pk,
            'SK': sk
        }
    ) 
    print(table_response)
    return table_response


def lambda_handler(event, context):
    print(event)
    body = json.loads(event['body'])
    pk = body['pk']
    sk = body['sk']
    try:
        response = read_post(pk,sk)
        item = response['Item']
        print(item)
        return{
            'statusCode': 200,
            'body': json.dumps({
                'message': 'single item',
                "item": item
            })
        }
    except ValidationError as e:
        return{
            'statusCode': 400,
            'body': json.dumps({
                'message': str(e)
            })
        }