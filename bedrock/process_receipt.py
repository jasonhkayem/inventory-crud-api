import boto3
import json
from botocore.exceptions import ClientError

def process_receipt(pdf_bytes, name):
    # Set up Bedrock runtime client
    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    # Hardcoded model ID (Claude 3 Sonnet)
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

    # Construct the conversation payload
    conversation = [
        {
            "role": "user",
            "content": [
                {
                    "text": (
                        "You are a receipt parser. Extract all product line items from this receipt "
                        "and return a structured JSON object with the following keys:\n\n"
                        "`items`: a list of purchased products (name, quantity, price),\n"
                        "`store`: the name of the store (if available),\n"
                        "`date`: the date of the receipt,\n"
                        "`total_amount`: the total amount paid.\n\n"
                        "Respond ONLY with JSON. Do not include any explanation or commentary."
                    )
                },
                {
                    "document": {
                        "format": "pdf",
                        "name": name,
                        "source": {"bytes": pdf_bytes},
                    }
                },
            ],
        }
    ]

    try:
        # Send the message to the model
        response = client.converse(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={
                "maxTokens": 1000,
                "temperature": 0.3,
            },
        )

        # Extract text content from response
        content_list = response["output"]["messages"][0]["content"]
        text_response = next(
            item["text"] for item in content_list if "text" in item
        )

        print("Claude response:", text_response)

        # Parse it as JSON
        return json.loads(text_response)

    except (ClientError, Exception) as e:
        print(f"ERROR: Failed to invoke Claude. Reason: {e}")
        raise
