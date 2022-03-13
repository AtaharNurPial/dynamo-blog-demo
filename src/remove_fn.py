import json
import boto3
import os

from pydantic import ValidationError
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')
table = dynamodb.Table(table_name)

def remove_post(pk,sk):
    table_response = table.delete_item(
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
        response = remove_post(pk,sk)
        print(response)
        return{
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Deleted single item',
            })
        }
    except ValidationError as e:
        return{
            'statusCode': 400,
            'body': json.dumps({
                'message': str(e)
            })
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 400,
            'body': json.dumps({
            'message': 'Some error occured.Please try again.'
            })
        }