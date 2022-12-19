from constructs import Construct
from aws_cdk import (
    aws_lambda as _lambda,
    aws_dynamodb as ddb,
    RemovalPolicy
)


class HitCounter(Construct):

    @property
    def handler(self):
        return self._handler

    @property
    def table(self):
        return self._table

    def __init__(self, scope: "Construct", id: 
        str, downstream: _lambda.IFunction, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self._table = ddb.Table(
            self, 'Hits',
            # https://beabetterdev.com/2022/02/07/dynamodb-partition-key-vs-sort-key/
            # TLDR: partition key is like a primary key for dynamodb and is required
            partition_key={'name': 'path', 'type': ddb.AttributeType.STRING},
            removal_policy=RemovalPolicy.DESTROY
        )

        self._handler = _lambda.Function(
            self, 'HitCountHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler='hitcount.handler',
            code=_lambda.Code.from_asset('lambda'),
            # table_name and function_name are `late-bound values`;
            #  properties that are only resolved when stack is deployed
            environment={
                'HITS_TABLE_NAME': self.table.table_name,
                'DOWNSTREAM_FUNCTION_NAME': downstream.function_name
            }
        )
        
        # must give lambda read/write permissions to our db table
        self.table.grant_read_write_data(self.handler)
        # must give this lambda permissions to invoke downstream lambda
        downstream.grant_invoke(self.handler)
