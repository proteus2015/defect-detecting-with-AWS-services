import json
import boto3
import os

# Create an SQS client
sqs = boto3.client('sqs')
queue_url = os.environ.get('anormoly_queue_url')

print('que url: ' + queue_url)


def lambda_handler(event, context):
    try:
        for record in event['Records']:
            payload = record['body']
            print(payload)
            return {
                'statusCode': 200,
                'defectMsg': json.dumps(payload)
            }

    except Exception as e:
        print(f"Error: {str(e)}")
        # Handle error scenarios and return an appropriate response

