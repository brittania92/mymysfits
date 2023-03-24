
from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_cloudfront as cloudfront, 
    aws_iam as iam,
    aws_s3 as s3,
    aws_s3_deployment as s3Deploy,
    CfnOutput as output, 
    aws_ecr as ecr,
    aws_ecr_assets as ecr_image,
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_ssm as ssm,
    aws_elasticloadbalancingv2 as elb,
    aws_apigatewayv2_alpha as apigw,
    aws_apigatewayv2 as apigwv2,
    aws_apigatewayv2_integrations_alpha as httpIntegrations,
    aws_lambda_python_alpha as lambdaPython,
    aws_lambda as awsLambda,
    aws_dynamodb as ddb,
    aws_logs as logs,
    CfnResource as CfnResource
)

from constructs import Construct
from os import environ as env
import boto3

class WebStack(Stack):

    def __init__(
        self, 
        scope: Construct, 
        construct_id: str,
        app_name: str,
        **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        hostBucket = s3.Bucket(
            self,
            "hostingBucket",
            website_index_document='index.html',
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        origin = cloudfront.OriginAccessIdentity(
            self,
            "s3origin",
            comment='CodeCatalystTutorialBlueprint'
        )

        #Grant origin read permissions
        hostBucket.grant_read(
            iam.CanonicalUserPrincipal(
                origin.cloud_front_origin_access_identity_s3_canonical_user_id)
            )

        originConfig = cloudfront.SourceConfiguration(
            
            behaviors=[
                cloudfront.Behavior(is_default_behavior=True)
            ],
            
            s3_origin_source=cloudfront.S3OriginConfig(
                s3_bucket_source=hostBucket,
                origin_access_identity=origin,
                origin_path='/web'
            )
        )

        cdn = cloudfront.CloudFrontWebDistribution(
            self,
            "CloudFront",
            viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.ALLOW_ALL,
            price_class=cloudfront.PriceClass.PRICE_CLASS_ALL,
            origin_configs=[originConfig]
        )

        #TODO: Issue: https://github.com/aws/aws-cdk/issues/19257.  Cross Stck 
        #dependency is broken X-stack.  Using Params for now

        endpoint = ssm.StringParameter.from_string_parameter_attributes(
            self,
            "apiEndpointSSMParam",
            parameter_name=f"/{app_name}/apiEndpoint"
        ).string_value

        indexdeployment = s3Deploy.BucketDeployment(
            self,
            'IndexDeployment',
            sources=[s3Deploy.Source.asset('./web/build'), s3Deploy.Source.asset('./web/public')],
            destination_bucket=hostBucket,
            distribution=cdn,
            destination_key_prefix='web',
            distribution_paths=['/web'],
            retain_on_delete=False
        )

        cloudfrontUrl = output(
            self,
            "endpointUrl",
            value=f'https://{cdn.distribution_domain_name}'
        )


class ServerlessAppStack(Stack):

    def __init__(
        self, 
        scope: Construct, 
        construct_id: str,
        app_name: str,
        **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ddb_table = ddb.Table(
            self,
            "app_table",
            removal_policy=RemovalPolicy.DESTROY,
            table_name=app_name,
            partition_key=ddb.Attribute(
                name="Name",
                type=ddb.AttributeType.STRING
            )  
        )

        ddb_table.add_global_secondary_index(
            index_name="LawChaosIndex",
            partition_key=ddb.Attribute(
                name='LawChaos',
                type=ddb.AttributeType.STRING
            ),
            sort_key=ddb.Attribute(
                name='Name',
                type=ddb.AttributeType.STRING
            ),
            read_capacity=5,
            write_capacity=5,
            projection_type=ddb.ProjectionType.ALL
        )

        ddb_table.add_global_secondary_index(
            index_name="GoodEvilIndex",
            partition_key=ddb.Attribute(
                name='GoodEvil',
                type=ddb.AttributeType.STRING
            ),
            sort_key=ddb.Attribute(
                name='Name',
                type=ddb.AttributeType.STRING
            ),
            read_capacity=5,
            write_capacity=5,
            projection_type=ddb.ProjectionType.ALL
        )

        lambda_function = lambdaPython.PythonFunction(
            self,
            'lambdaFunction',
            entry='./src',
            runtime=awsLambda.Runtime.PYTHON_3_9,
            index='app.py',
            handler='handler',
            environment={
                'APPNAME': app_name,
                'FORCE_UPDATE': "True"
            }
        )

        ddb_table.grant_read_write_data(lambda_function)

        endpoint_proxy = apigw.HttpApi(
            self,
            app_name
        )

        lambda_integration = httpIntegrations.HttpLambdaIntegration(
            "LambdaIntegration",
            lambda_function
        )

        endpoint_proxy.add_routes(
            path = '/{proxy+}',
            methods=[apigw.HttpMethod.ANY],
            integration=lambda_integration
        )

        ssm.StringParameter(
            self,
            "apiEndpointSSMParam",
            parameter_name=f"/{app_name}/apiEndpoint",
            string_value=endpoint_proxy.url[:-1]
        )

        api_url = output(
            self,
            'apiUrl',
            value=endpoint_proxy.url
        )

class ContainerAppStack(Stack):

    def __init__(self,
        scope: Construct, 
        construct_id: str, 
        app_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.SERVICE_PORT = 8080

        vpc = ec2.Vpc.from_lookup(self,
            "Vpc",
            is_default=True    
        )

        ddb_table = ddb.Table(
            self,
            "app_table",
            removal_policy=RemovalPolicy.DESTROY,
            table_name=app_name,
            partition_key=ddb.Attribute(
                name="Name",
                type=ddb.AttributeType.STRING
            )  
        )

        ddb_table.add_global_secondary_index(
            index_name="LawChaosIndex",
            partition_key=ddb.Attribute(
                name='LawChaos',
                type=ddb.AttributeType.STRING
            ),
            sort_key=ddb.Attribute(
                name='Name',
                type=ddb.AttributeType.STRING
            ),
            read_capacity=5,
            write_capacity=5,
            projection_type=ddb.ProjectionType.ALL
        )

        ddb_table.add_global_secondary_index(
            index_name="GoodEvilIndex",
            partition_key=ddb.Attribute(
                name='GoodEvil',
                type=ddb.AttributeType.STRING
            ),
            sort_key=ddb.Attribute(
                name='Name',
                type=ddb.AttributeType.STRING
            ),
            read_capacity=5,
            write_capacity=5,
            projection_type=ddb.ProjectionType.ALL
        )

        ecrRepo = ecr.Repository(
            self,
            "AppContainerRepo",
            repository_name=app_name.lower(),
            removal_policy=RemovalPolicy.DESTROY
        )

        image = ecr_image.DockerImageAsset(
            self,
            "DockerImage",
            directory='./'
        )

        ecsCluster = ecs.Cluster(
            self,
            "EcsCluster",
            vpc=vpc,
        )

        taskDefinitionPolicy = iam.PolicyStatement()
        taskDefinitionPolicy.add_actions(
            "ec2:AttachNetworkInterface",
            "ec2:CreateNetworkInterface",
            "ec2:CreateNetworkInterfacePermission",
            "ec2:DeleteNetworkInterface",
            "ec2:DeleteNetworkInterfacePermission",
            "ec2:Describe*",
            "ec2:DetachNetworkInterface",
            "elasticloadbalancing:DeregisterInstancesFromLoadBalancer",
            "elasticloadbalancing:DeregisterTargets",
            "elasticloadbalancing:Describe*",
            "elasticloadbalancing:RegisterInstancesWithLoadBalancer",
            "elasticloadbalancing:RegisterTargets",
            "iam:PassRole",
            "logs:DescribeLogStreams",
            "logs:CreateLogGroup",
            "ecr:GetAuthorizationToken",
            "ecr:BatchCheckLayerAvailability",
            "ecr:GetDownloadUrlForLayer",
            "ecr:BatchGetImage",
            "logs:CreateLogStream",
            "logs:CreateLogGroup",
            "logs:PutLogEvents",
            "dynamodb:Scan",
            "dynamodb:Query",
            "dynamodb:UpdateItem",
            "dynamodb:GetItem",
            "dynamodb:DescribeTable",
            "dynamodb:PutItem"
        )
        
        taskDefinitionPolicy.add_all_resources()

        service_role = iam.Role(
            self,
            'ecsServiceRole',
            assumed_by=iam.ServicePrincipal('ecs-tasks.amazonaws.com')
        )

        service_role.add_to_policy(taskDefinitionPolicy)

        log_group = logs.LogGroup(
            self,
            'appLogGroup',
            removal_policy=RemovalPolicy.DESTROY
        )

        log_driver = ecs.AwsLogDriver(
            log_group=log_group,
            stream_prefix='service'
        )
        
        service_sg = ec2.SecurityGroup(
            self,
            'serviceSG',
            vpc=vpc,
            allow_all_outbound=True,
        )
        service_sg.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(self.SERVICE_PORT),
            'Allow alt web port'
            )

        esc_task_def = ecs.TaskDefinition(
            self, 
            'ecsTaskDef',
            memory_mib="1024",
            cpu="512",
            compatibility=ecs.Compatibility.FARGATE,
            task_role=service_role,
            execution_role=service_role
        )

        esc_task_def.add_container(
            'taskdefcontainer',
            image=ecs.EcrImage.from_docker_image_asset(image),
            logging=log_driver,
            port_mappings=[{'containerPort': self.SERVICE_PORT}],
            environment={
                "AWS_DEFAULT_REGION": env.get("CDK_DEFAULT_REGION"),
                "APPNAME": app_name,
                'FORCE_UPDATE': "True"
            }    
        )

        fargate_service = ecs.FargateService(
            self,
            'fargateService',
            cluster=ecsCluster,
            task_definition=esc_task_def,
            assign_public_ip=True,
            desired_count=2,
            security_groups=[service_sg]
        )

        service_nlb = elb.NetworkLoadBalancer(
            self,
            'serviceNLB',
            internet_facing=False,
            vpc=vpc
        )

        service_listener = service_nlb.add_listener(
            'serviceListener',
            port=self.SERVICE_PORT
        )

        service_listener.add_targets(
            'targetGroup',
            port=self.SERVICE_PORT,
            targets=[fargate_service]
        )

        endpoint_proxy = apigw.HttpApi(
            self,
            app_name
        )

        vpc_link = CfnResource(
            self,
            'vpcLink',
             type="AWS::ApiGatewayV2::VpcLink",
             properties={
                 "Name": Stack.of(self).stack_name,
                 "SubnetIds": [v.subnet_id for v in vpc.public_subnets]
            }
        )

        integration = apigwv2.CfnIntegration(
            self,
            'proxyIntegration',
            api_id=endpoint_proxy.api_id,
            integration_type="HTTP_PROXY",
            connection_id=vpc_link.ref,
            connection_type="VPC_LINK",
            description="API Integration",
            integration_method="ANY",
            integration_uri=service_listener.listener_arn,
            payload_format_version="1.0"   
        )

        route = apigwv2.CfnRoute(
            self,
            'intRoute',
            api_id=endpoint_proxy.api_id,
            route_key="ANY /{proxy+}",
            target=f'integrations/{integration.ref}',
        )

        ssm.StringParameter(
            self,
            "apiEndpointSSMParam",
            parameter_name=f"/{app_name}/apiEndpoint",
            string_value=endpoint_proxy.url
        )

        api_url = output(
            self,
            'apiUrl',
            value=endpoint_proxy.url
        )
       