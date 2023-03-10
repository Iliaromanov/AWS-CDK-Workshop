import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import { Construct } from 'constructs';

export interface HitCounterProps {
    downstream: lambda.IFunction;
}

export class HitCounter extends Construct {
    
    /** allows accessing the counter function */
    // similar to @property of python class
    public readonly handler: lambda.Function;

    /** allows accessing the hitcounter dynamo table */
    public readonly table: dynamodb.Table;

    constructor(scope: Construct, id: string, props: HitCounterProps) {
        super(scope, id);
        
        this.table = new dynamodb.Table(this, 'Hits', {
            partitionKey: {
                name: 'path', type: dynamodb.AttributeType.STRING
            },
            removalPolicy: cdk.RemovalPolicy.DESTROY
        });

        this.handler = new lambda.Function(
            this, 'HitCounterHandler', {
                runtime: lambda.Runtime.NODEJS_14_X,
                code: lambda.Code.fromAsset('lambda'),
                handler: 'hitcounter.handler',
                environment: {
                    DOWNSTREAM_FUNCTION_NAME: props.downstream.functionName,
                    HITS_TABLE_NAME: this.table.tableName
                }
            }
        );

        // must give lambda read/write permissions to db table
        this.table.grantReadWriteData(this.handler);

        // must give hitcounter lambda permissions to invoke downstream lambda
        props.downstream.grantInvoke(this.handler);
    }
}