import os
import json
from constructs import Construct
from aws_cdk import (
    Stack,
    Duration,
    RemovalPolicy,
    aws_apigateway as apigateway,
    aws_lambda as lambda_,
    aws_events as events,
    aws_events_targets as targets,
    aws_dynamodb as dynamodb,
)


class BotStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Add Lambda function
        fastapi_cdk_function = lambda_.Function(
            self,
            "ConcertTelegramBot",
            code=lambda_.Code.from_asset_image("./assets"),
            handler=lambda_.Handler.FROM_IMAGE,
            runtime=lambda_.Runtime.FROM_IMAGE,
            environment={
                "BOT_TOKEN": os.getenv(key="BOT_TOKEN"),
                "CHAT_ID": os.getenv(key="CHAT_ID"),
            },
            timeout=Duration.seconds(30),
        )

        # Add API Gateway
        api = apigateway.RestApi(
            self,
            "ConcertTelegramBotAPI",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS,
            ),
            deploy_options=apigateway.StageOptions(
                throttling_rate_limit=2,  # Requests per second
                throttling_burst_limit=5  # Max concurrent requests
            )
        )

        # Add a resource to the API Gateway
        fastapi_cdk_function_integration = apigateway.LambdaIntegration(
            fastapi_cdk_function, allow_test_invoke=False
        )

        # Add a method to the resource
        api.root.add_method("ANY", fastapi_cdk_function_integration)

        api.root.add_proxy(
            default_integration=apigateway.LambdaIntegration(
                fastapi_cdk_function, allow_test_invoke=False
            ),
            any_method=True,
        )

        # Add a DynamoDB table
        events_table = dynamodb.Table(
            self, 'EventsTable',
            partition_key=dynamodb.Attribute(
                name="event_id",
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY,  # This will delete the table when the stack is destroyed. Be cautious with this in production.
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST  # Use on-demand pricing. Adjust according to your needs.
        )

        # Grant the Lambda function permission to read/write to the DynamoDB table
        events_table.grant_read_write_data(fastapi_cdk_function)

        # Add DynamoDB table name to Lambda environment variables
        fastapi_cdk_function.add_environment("EVENTS_TABLE", events_table.table_name)
        
        # Schedule Lambda function with EventBridge
        rule = events.Rule(
            self,
            "Rule",
            schedule=events.Schedule.cron(
                minute="0",  # At minute 0
                hour="9,15,21",  # At 9:00 AM, 3:00 PM, and 9:00 PM UTC
                # Leaving day-of-month, month, and day-of-week as '*' to run every day
            ),
        )

        # Add default data for the trigger
        default_event = {
            "body": json.dumps({
                "message": {
                    "text": "/scrape",
                    "chat": {
                        "id": os.getenv(key="CHAT_ID"),
                        "first_name": "Ali"
                    }
                }
            })
        }

        rule.add_target(targets.LambdaFunction(fastapi_cdk_function,
                                               event=events.RuleTargetInput.from_object(default_event)))
