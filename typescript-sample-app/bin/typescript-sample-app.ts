#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { TypescriptSampleAppStack } from '../lib/typescript-sample-app-stack';

const app = new cdk.App();
new TypescriptSampleAppStack(app, 'TypescriptSampleAppStack');
