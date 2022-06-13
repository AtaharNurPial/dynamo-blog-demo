import boto3
import os, json
from pydantic import ValidationError
from BaseModel import base_model

from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver
from aws_lambda_powertools import Logger, Metrics
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.logging import correlation_paths

logger = Logger(service="Powertool_Logger")
metrics = Metrics(namespace="blog-demo-app", service="Powertool_Metric")


app = ApiGatewayResolver()

dynamodb = boto3.resource("dynamodb")
table_name = os.environ.get("TABLE_NAME")
table = dynamodb.Table(table_name)


def add_post(blog_item):
    table_response = table.put_item(TableName=table_name, Item=blog_item.dict())
    logger.info(f"Request for adding a new post received...")
    metrics.add_metric(name="PostAdded", unit=MetricUnit.Count, value=1)
    print(table_response)
    return {"message": f"adding the new{table_response}"}


@logger.inject_lambda_context(
    correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True
)
@metrics.log_metrics(capture_cold_start_metric=True)
def lambda_handler(event, context):
    result = app.resolve(event, context)
    print(event)
    body = json.loads(event["body"])
    blog_item = base_model.Blog_Item(**body)
    try:
        response = add_post(blog_item)
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "post added successfully",
                    "value": blog_item.dict(),
                    "result": result,
                }
            ),
        }
    except ValidationError as e:
        return {"statusCode": 400, "body": json.dumps({"message": str(e)})}
    except Exception as e:
        logger.exception(e)
        raise
