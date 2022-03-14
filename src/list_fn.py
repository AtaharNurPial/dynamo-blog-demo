import os, json
import boto3
from pydantic import ValidationError
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')
index_name = os.environ.get('INDEX_NAME')
table = dynamodb.Table(table_name)

def list_post(publish_date):
    table_response = table.query(
        TableName = table_name,
        IndexName = index_name,
        KeyConditionExpression=Key('publish_date').eq(publish_date)
    )
    print(table_response)
    return table_response

def lambda_handler(event, context):
    print(event)
    body = json.loads(event['body'])
    publish_date = body['publish_date']
    try:
        response = list_post(publish_date)
        print(response)
        items = response['Items']
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