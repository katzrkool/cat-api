from helpers import verify_body, verify_headers, return_response, MANDATORY_ATTRIBUTES
import boto3
import uuid
import os

TABLE_NAME = os.environ["TABLE_NAME"]

def create_cat(event, context):

    ### Incoming event verification
    if not verify_headers(event):
        return return_response(400, "Bad headers")
    result, body = verify_body(event, MANDATORY_ATTRIBUTES)
    if not result:
        return return_response(400, body)
    ### Verification ends here

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)
    cat = {
        "id": str(uuid.uuid4()),
        "info": {
            "name": str(body["name"]),
            "age": str(body["age"]),
            "description": str(body["description"])
        }
    }
    table.put_item(Item=cat)
    return return_response(201, cat)