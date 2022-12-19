from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
)

from .hitcounter import HitCounter

class PythonSampleAppStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        my_lambda = _lambda.Function(
            self, "HelloLambda",
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset("lambda"),
            handler="hello.handler"
        )

        hello_with_hitcounter = HitCounter(
            self, 'HitCounter',
            downstream=my_lambda,
        )

        apigw.LambdaRestApi(
            self, "Endpoint",
            handler=hello_with_hitcounter.handler
        )
