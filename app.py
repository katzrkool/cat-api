from aws_cdk import core
from cloudformation.cat_api_stack import CatApiStack


app = core.App()
CatApiStack(app, "CatApiStack")

app.synth()