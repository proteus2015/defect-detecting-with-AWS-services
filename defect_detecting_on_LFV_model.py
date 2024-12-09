import boto3
import json
import time
from datetime import datetime
import urllib.parse


def lambda_handler(event, context):
    # TODO implement

    # Create an SNS client
    sns_client = boto3.client('sns')
    sns_topic_arn = "arn:aws:sns:us-west-2:XXXXXXXXXXXXXXXXX"

    # Initialize the S3 client
    s3_client = boto3.client("s3")
    print(event)
    # S3_BUCKET = "defect-detecting-poc";

    S3_BUCKET = event['Records'][0]['s3']['bucket']['name']
    object_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

    # Your custom processing logic here
    # For demonstration purposes, let's just print the object key
    print(f"New object uploaded to bucket '{S3_BUCKET}': {object_key}")

    # intialize the dynamoDB table
    print("set up dynamoDB connection:")
    dynamodb = boto3.resource("dynamodb")
    table_name = "defect-detecting-poc"
    print("Retrieving image from S3")
    # object_key = "In_1.jpg"

    try:
        # Read the file content from S3
        file_content = s3_client.get_object(Bucket=S3_BUCKET, Key=object_key)["Body"].read()

        # Process the file content (e.g., print it)
        # print(file_content)

        lookout_client = boto3.client("lookoutvision")

        # Specify project name, model version, content type, and image data
        project_name = "defect-detecting-poc"
        model_version = "4"

        min_inference_units = 1

        # this is to avoid starting 2 models at the same time
        # stop_model_response=lookout_client.stop_model(ProjectName=project_name, ModelVersion=model_version)
        # print('Stop Model Status: ' + stop_model_response['Status'])

        start_model(lookout_client, project_name, model_version, min_inference_units)

        content_type = "image/jpeg"  # or "image/png"
        image_data = file_content

        # Call DetectAnomalies
        response = lookout_client.detect_anomalies(
            ProjectName=project_name,
            ModelVersion=model_version,
            ContentType=content_type,
            Body=image_data
        )

        Anomaly_prediction = response["DetectAnomalyResult"]["IsAnomalous"]
        Confidence = response["DetectAnomalyResult"]["Confidence"]

        print('Stopping model version ' + model_version + ' for project ' + project_name)
        stop_model_response = lookout_client.stop_model(ProjectName=project_name, ModelVersion=model_version)
        print('Stop Model Status: ' + stop_model_response['Status'])

        print(f"detect result of '{object_key}': {Anomaly_prediction}, {Confidence}")

        if Anomaly_prediction is True:
            # write to dynamoDB
            timestamp = int(time.time())
            df = datetime.fromtimestamp(timestamp)
            item = {
                "defectId": object_key
                # "timestamp":timestamp,

            }
            print("item:")
            print(item)

            table = dynamodb.Table(table_name)
            table.put_item(Item=item)

            print("Timestamp {timestamp} added to DynamoDB table {table_name}")

            print('Starting sending message to sns ' + sns_topic_arn + ' for a message ' + object_key)
            send_sns(sns_client, object_key, sns_topic_arn)

        # return tuple ("detect result", Anomaly_prediction,Confidence)
        result = {
            "datetime": df.strftime('%m/%d/%Y, %H:%M:%S'),
            "defectId": object_key
        }
        return result

    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error retrieving image: {str(e)}"
        }


def start_model(lookoutvision_client, project_name, model_version, min_inference_units, max_inference_units=None):
    """
    Starts the hosting of a Lookout for Vision model.

    :param lookoutvision_client: A Boto3 Lookout for Vision client.
    :param project_name:  The name of the project that contains the version of the
                          model that you want to start hosting.
    :param model_version: The version of the model that you want to start hosting.
    :param min_inference_units: The number of inference units to use for hosting.
    :param max_inference_units: (Optional) The maximum number of inference units that
    Lookout for Vision can use to automatically scale the model.
    """
    try:
        print(f"Starting model version '{model_version}' for project '{project_name}'")

        if max_inference_units is None:
            lookoutvision_client.start_model(
                ProjectName=project_name,
                ModelVersion=model_version,
                MinInferenceUnits=min_inference_units)

        else:
            lookoutvision_client.start_model(
                ProjectName=project_name,
                ModelVersion=model_version,
                MinInferenceUnits=min_inference_units,
                MaxInferenceUnits=max_inference_units)

        print("Starting hosting...")

        status = ""
        finished = False

        # Wait until hosted or failed.
        while finished is False:
            model_description = lookoutvision_client.describe_model(
                ProjectName=project_name, ModelVersion=model_version)
            status = model_description["ModelDescription"]["Status"]

            if status == "STARTING_HOSTING":
                print("Host starting in progress...")
                time.sleep(10)
                continue

            if status == "HOSTED":
                print("Model is hosted and ready for use.")
                finished = True
                continue

            print("Model hosting failed and the model can't be used.")
            finished = True

        if status != "HOSTED":
            print("Error hosting model: %s", status)

    except Exception as error:
        print("there is an except", error)


def send_sns(sns_client, message, sns_topic_arn):
    try:
        response = sns_client.publish(
            TargetArn=sns_topic_arn,
            Message=json.dumps({'default': json.dumps(message)}),
            MessageStructure='json')

        print("Message published")

    except Exception as error:
        print("there is an except", error)