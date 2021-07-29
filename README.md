## The CAT Api
### Deployment to AWS using AWS CDK and Github Actions
___
Author: Edvinas Bosas
___

This creates a REST API with:
* DynamoDB Table
* 4 Lambda Functions
* 4 API Gateway Endpoints, each associated with a different Lambda function:
    * POST /create
    * GET /list
    * PUT /update
    * DELETE /delete

---

### Expected incoming JSON structure for /create and /update endpoints
Required headers: `Content-Type: application/json`
* POST /create:
    ~~~json
    {
        "name": "string",
        "age": "string",
        "description": "string"
    }
    ~~~
* PUT /update:
    * `PUT /update` URI must point to a specific cat: `PUT /update?id={uuid}`
    ~~~json
    {
        "name": "string",
        "age": "string",
        "description": "string"
    }
    ~~~

### Expected URL parameter structure for /list and /delete endpoints

* /list

    * Simply calling `GET /list` endpoint returns all cat entries in the database.

    * Calling `GET /list?id={uuid}` will return a specific cat from the database.

    * `{uuid}` can be multiple comma seperated values: `GET /list?id={uuid1},{uuid2}`

* /delete

    * Requires a single `{uuid}` parameter: `DELETE /delete?id={uuid}`
