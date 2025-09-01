import boto3
from flask import json

def invoke_bedrock_embedding(text: str) -> list[float]:
    """
    Invoke Amazon Bedrock Titan Text Embedding Model to generate embeddings.

    ---
    parameters:
      - name: text
        in: body
        type: string
        required: true
        description: Input text string to generate embedding for.
    responses:
      200:
        description: List of floats representing the embedding vector.
        schema:
          type: array
          items:
            type: number
            format: float
      500:
        description: Error occurred while invoking Bedrock.
    """
    bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")
    if not text:
        return []

    payload = {"inputText": text}

    try:
        response = bedrock_client.invoke_model(
            modelId='amazon.titan-embed-text-v2:0',
            contentType='application/json',
            body=json.dumps(payload)
        )
        response_body = response['body'].read()
        embedding_result = json.loads(response_body)
        print("Embedding:", embedding_result.get('embedding', []))
        return embedding_result.get('embedding', [])
    except Exception as e:
        print(f"Bedrock invocation failed: {e}")
        raise