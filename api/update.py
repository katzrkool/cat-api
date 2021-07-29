from helpers import verify_params, verify_headers, verify_body, return_response, MANDATORY_ATTRIBUTES
import boto3
import os

TABLE_NAME = os.environ["TABLE_NAME"]

def update_cat(event, context):

    ### Verify query string params and JSON body
    if not verify_headers(event):
        return return_response(400, "Bad headers")
    result, id_ = verify_params(event, single_needed=True, empty_ok=False)
    if not result:
        return return_response(400, "Bad or missing query parameter")
    result, body = verify_body(event, MANDATORY_ATTRIBUTES)
    if not result:
        return return_response(400, body)
    ### Verification ends here

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(TABLE_NAME)
    cat = table.get_item(Key={"id": id_})
    if not cat.get("Item"):
        return return_response(404, "No cat found")
    item = {
        "name": str(body["name"]),
        "age": str(body["age"]),
        "description": str(body["description"])
    }
    table.update_item(
        Key={"id": id_},
        UpdateExpression="SET info = :newInfo",
        ExpressionAttributeValues={
            ":newInfo": item
        }
    )
    return return_response(200, item)