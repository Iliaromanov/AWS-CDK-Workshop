from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda,
    aws_apigateway as apigw,
)


class PythonSampleAppStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        my_lambda = aws_lambda.Function(
            self, "HelloLambda",
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            code=aws_lambda.Code.from_asset("lambda"),
            handler="hello.handler"
        )

        apigw.LambdaRestApi(
            self, "Endpoint",
            handler=my_lambda
        )
