import boto3
from botocore.exceptions import ClientError
from flask import json


def invoke_bedrock_category(product_name: str) -> str:
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    prompt = f"Classify this product in a category: '{product_name}'. Provide only the category name."

    native_request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 512,
        "temperature": 0.5,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}],
            }
        ],
    }

    request = json.dumps(native_request)

    try:
        response = client.invoke_model(modelId=model_id, body=request)
    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        return None

    model_response = json.loads(response["body"].read())
    response_text = model_response["content"][0]["text"].strip()
    print(f"Bedrock response: {response_text}")
    return response_text
