from helpers import verify_params, return_response
import boto3
import os

TABLE_NAME = os.environ["TABLE_NAME"]

def delete_cat(event, context):
    
    ### Verify query string parameters
    result, id_ = verify_params(event, single_needed=True, empty_ok=False)
    if not result:
        return return_response(400, "Bad or missing query parameter")
    ### Verification ends here

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(TABLE_NAME)
    cat = table.get_item(Key={"id": id_})
    if not cat.get("Item"):
        return return_response(404, "No cat found")
    table.delete_item(Key={"id": id_})
    return return_response(200, f"{id_} has been deleted")