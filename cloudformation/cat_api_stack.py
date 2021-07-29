from aws_cdk import core as cdk
from aws_cdk import aws_dynamodb
from aws_cdk import aws_lambda
from aws_cdk import aws_apigateway


class CatApiStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a 'Cats' table with a single primary key 'id'
        table = aws_dynamodb.Table(self, "Cats", partition_key=aws_dynamodb.Attribute(name="id", type=aws_dynamodb.AttributeType.STRING))

        # Create Lambda functions
        create = aws_lambda.Function(
            self, "CreateHandler",
            code=aws_lambda.Code.from_asset("./api"),
            handler="create.create_cat",
            runtime=aws_lambda.Runtime.PYTHON_3_8
        )
        list = aws_lambda.Function(
            self, "ListHandler",
            code=aws_lambda.Code.from_asset("./api"),
            handler="list.list_cat",
            runtime=aws_lambda.Runtime.PYTHON_3_8
        )

        update = aws_lambda.Function(
            self, "UpdateHandler",
            code=aws_lambda.Code.from_asset("./api"),
            handler="update.update_cat",
            runtime=aws_lambda.Runtime.PYTHON_3_8
        )

        delete = aws_lambda.Function(
            self, "DeleteHandler",
            code=aws_lambda.Code.from_asset("./api"),
            handler="delete.delete_cat",
            runtime=aws_lambda.Runtime.PYTHON_3_8
        )

        # Inject table name into Lambda functions as environment variable
        for handler in [create, update, list, delete]:
            handler.add_environment("TABLE_NAME", table.table_name)
        
        # Grant appropriate read/write permissions to Lambda functions
        table.grant_write_data(create)
        table.grant_read_data(list)
        table.grant_read_write_data(update)
        table.grant_read_write_data(delete)

        # Create an API Gateway with appropriate resources
        api = aws_apigateway.RestApi(self, "CatApi", rest_api_name="CatApi", description="API for Cats")
        create_cat = api.root.add_resource("create")
        list_cat = api.root.add_resource("list")
        update_cat = api.root.add_resource("update")
        delete_cat = api.root.add_resource("delete")

        # Integrate Lambda functions to API Gateway
        create_handler = aws_apigateway.LambdaIntegration(create)
        list_handler = aws_apigateway.LambdaIntegration(list)
        update_handler = aws_apigateway.LambdaIntegration(update)
        delete_handler = aws_apigateway.LambdaIntegration(delete)

        # Add integrated Lambda functions to handle specific requests to API resources
        create_cat.add_method("POST", create_handler)
        list_cat.add_method("GET", list_handler)
        update_cat.add_method("PUT", update_handler)
        delete_cat.add_method("DELETE", delete_handler)

