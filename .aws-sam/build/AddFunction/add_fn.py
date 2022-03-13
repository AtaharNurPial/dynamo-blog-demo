import boto3
import os, json
from pydantic import ValidationError
from BaseModel import base_model

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')
table = dynamodb.Table(table_name)

def add_post(blog_item):
    table_response = table.put_item(
        TableName = table_name,
        Item=blog_item.dict()
    )
    print(table_response)
    return table_response

def lambda_handler(event, context):
    print(event)
    body = json.loads(event['body'])
    blog_item = base_model.Blog_Item(**body)
    # print(type(body))
    try:
        response = add_post(blog_item)
        return{
            'statusCode': 200,
            'body': json.dumps({
                'message': 'post added successfully',
                'value': blog_item.dict()
            })
        }
    except ValidationError as e:
        return{
            'statusCode': 400,
            'body': json.dumps({
                'message': str(e)
            })
        }
