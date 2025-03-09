# from typing import Any
import pulumi
import pulumi_aws as aws
import pulumi_awsx as awsx
import json

# First, create an API Gateway
api_gateway = aws.apigatewayv2.Api("app-api",
    name="Ticket Server Lambda API",
    protocol_type="HTTP",
    route_selection_expression="$request.method $request.path"
)

# Create IAM role for Lambda
lambda_role = aws.iam.Role("lambda-app-role",
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Effect": "Allow",
            "Sid": ""
        }]
    })
)

# Attach basic execution policy - Lambda needs this to write logs
lambda_role_policy: aws.iam.RolePolicyAttachment = aws.iam.RolePolicyAttachment("lambda-role-policy",
    role=lambda_role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
)

# Create ECR repository for our container
repository = aws.ecr.Repository("ticket-server-app-repo",
    name="ticket-server-app-repo",
    force_delete=True,  # Makes cleanup easier for testing
    image_scanning_configuration=aws.ecr.RepositoryImageScanningConfigurationArgs(
        scan_on_push=True,
    )
)

# Build and push the Docker image to ECR
image = awsx.ecr.Image("app-image",
    repository_url=repository.repository_url,
    context="..", # Tells awsx to use the main directory as the build path
    dockerfile="../Dockerfile",  # Path to my Dockerfile
    platform="linux/amd64"  # Important for M1/M2 Mac users
)

# Create the Lambda function
lambda_function = aws.lambda_.Function("app-function",
    name="app-function",
    package_type="Image",
    image_uri=image.image_uri,
    role=lambda_role.arn,
    timeout=30,
    memory_size=512
)

# Create API Gateway stage
stage = aws.apigatewayv2.Stage("api-stage",
    api_id=api_gateway.id,
    name="$default",
    auto_deploy=True
)

# Connect API Gateway to Lambda
integration = aws.apigatewayv2.Integration("lambda-integration",
    api_id=api_gateway.id,
    integration_type="AWS_PROXY",
    integration_uri=lambda_function.arn,
    integration_method="POST",
    payload_format_version="2.0"
)

# Create catch-all route
route = aws.apigatewayv2.Route("catch-all-route",
    api_id=api_gateway.id,
    route_key="ANY /{proxy+}",
    target=integration.id.apply(lambda id: f"integrations/{id}")
)

# Allow API Gateway to invoke Lambda
lambda_permission = aws.lambda_.Permission("api-lambda-permission",
    action="lambda:InvokeFunction",
    function=lambda_function.name,
    principal="apigateway.amazonaws.com",
    source_arn=api_gateway.execution_arn.apply(lambda arn: f"{arn}/*/*")
)

# Export the API Gateway URL
pulumi.export("url", api_gateway.api_endpoint)