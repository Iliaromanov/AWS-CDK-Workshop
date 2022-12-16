#!/usr/bin/env python3

import aws_cdk as cdk

from python_sample_app.python_sample_app_stack import PythonSampleAppStack


app = cdk.App()
PythonSampleAppStack(app, "python-sample-app")

app.synth()
