#!/usr/bin/env python3
import os, time, json
from os import environ as env
import boto3

app_name="mysfitshz0r6"

import aws_cdk as cdk

from cdkStacks.stacks import (
     ServerlessAppStack, WebStack
)
app = cdk.App()

appStack = ServerlessAppStack(app, 
    app_name+"AppStack",
    env={
        "account": env.get('CDK_DEFAULT_ACCOUNT'),
        "region": env.get('CDK_DEFAULT_REGION')
    },
    app_name=app_name,
)

webStack = WebStack(app,
    app_name+"WebStack",
    env={
        "account": env.get('CDK_DEFAULT_ACCOUNT'),
        "region": env.get('CDK_DEFAULT_REGION')
    },
    app_name=app_name
)

app.synth()