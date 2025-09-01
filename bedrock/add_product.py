import os
import requests

from .description_generator import invoke_bedrock_description

api_url = os.getenv("INVENTORY_API_URL")

def add_product_receipt(data):
    for item in data.get("items", []):
        description = invoke_bedrock_description(item["name"])
        payload = {
            "name": item["name"],
            "quantity": item["quantity"],
            "price": item["price"],
            "description": description
        }

        response = requests.post(f"{api_url}/products/create", json=payload)
        if response.status_code != 201:
            print(f"Failed to add product: {item['name']}, Error: {response.text}")