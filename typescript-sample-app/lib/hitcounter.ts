import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import { Construct } from 'constructs';
import { Runtime } from 'aws-cdk-lib/aws-lambda';

export interface HitCounterProps {
    downstream: lambda.IFunction;
}

export class HitCounter extends Construct {
    
    /** allows accessing the counter function */
    // similar to @property of python class
    public readonly handler: lambda.Function;

    constructor(scope: Construct, id: string, props: HitCounterProps) {
        super(scope, id);
        
        const table = new dynamodb.Table(this, 'Hits', {
            partitionKey: { name: 'path', type: dynamodb.AttributeType.STRING }
        });

        this.handler = new lambda.Function(
            this, 'HitCountHandler', {
                runtime: lambda.Runtime.NODEJS_14_X,
                code: lambda.Code.fromAsset('lambda'),
                handler: 'hitcounter.handler',
                environment: {
                    DOWNSTREAM_FUNCTION_NAME: props.downstream.functionName,
                    HITS_TABLE_NAME: table.tableName
                }
            }
        );
    }
}