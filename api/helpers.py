import json

MANDATORY_ATTRIBUTES = ["name", "description", "age"]

def return_response(status_code, body):
    # Generic response template to be used in other functions
    response = {
        "statusCode": status_code,
        "body": json.dumps({
            "status_code": status_code,
            "data": body
        }, indent=4),
        "headers": {
            "Content-Type": "application/json"
        }
    }
    return response

def verify_headers(event, content_type="application/json"):
    # Some handlers require specific header types. Quickly check them with this
    if not event["headers"]["Content-Type"] == content_type:
        return False
    return True

def verify_body(event, attributes):
    # Verify whether incoming event contains correct JSON schema
    if not event["body"]:
        return False, "Missing JSON body"
    body = json.loads(event["body"])
    body = {key.lower(): value for key, value in body.items()}
    if any(attr not in body for attr in attributes):
        return False, "Missing mandatory JSON attributes"
    for attr in attributes:
        if not body.get(attr):
            return False, f"{attr} field is empty"
    return True, body

def verify_params(event, needed="id", single_needed=False, empty_ok=True):
    # Verify whether incoming event query parameters are correct for DB query
    params = event.get("queryStringParameters")
    if not params:
        if empty_ok:
            return True, None
        return False, None
    params = {key.lower(): value for key, value in params.items()}
    param = params.get(needed)
    if not param:
        return False, None
    ids = [id_.strip() for id_ in param.split(",")]
    if not single_needed:
        return True, ids
    if single_needed and len(ids) > 1:
        return False, None
    return True, ids[0]