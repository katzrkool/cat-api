from helpers import verify_headers, return_response, verify_params
import boto3
import os

TABLE_NAME = os.environ["TABLE_NAME"]

def list_cat(event, context):
    
    ### Verify query string params
    result, ids = verify_params(event)
    if not result:
        return return_response(400, "Bad query parameters provided")
    ### Verification ends here

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(TABLE_NAME)
    if result and ids is None:
        cats = table.scan()
        return return_response(200, cats["Items"])
    cats = []
    for id_ in ids:
        cat = table.get_item(Key={"id": id_})
        if cat.get("Item"):
            cats.append(cat["Item"])
    return return_response(200, cats)