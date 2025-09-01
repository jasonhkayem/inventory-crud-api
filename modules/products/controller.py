from flask import request, jsonify
from marshmallow import ValidationError

from .services import (
    classify_batch_service,
    generate_embedding_service,
    get_product_service,
    get_products_service,
    add_product_service,
    health_status_service,
    similarity_search_by_id_service,
    similarity_search_by_name_service,
    translate_name_description_service,
    update_product_service,
    delete_product_service,
    total_value_service,
    avg_product_price_service,
    min_max_price_service,
    total_nb_of_products_category_service,
    out_of_stock_service,
    most_expensive_products_service,
    value_per_category_service
)

from .validation import validate_input

from .middleware import BatchIDsSchema, ProductSchema


def add_product():
    """
    Controller to add a new product.

    - Extracts JSON data from the request.
    - Validates input using ProductSchema.
    - Returns 400 with errors if validation fails.
    - Calls the service layer to add the product with valid data.
    - Returns the newly created product as JSON with status 201.
    """
    data = request.get_json()

    valid_data, errors = validate_input(ProductSchema, data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    return jsonify(add_product_service(valid_data).to_dict()), 201


def get_products():
    """
    Controller to retrieve all products.

    - Calls the service layer to fetch all products.
    - Converts each product object to a dictionary.
    - Returns the list of product dictionaries as JSON with status 200.
    """
    products = get_products_service()
    products_list = [product.to_dict() for product in products]
    return jsonify(products_list), 200


def get_product(id):
    """
    Controller to retrieve a single product by its ID.

    Args:
        id (int): The ID of the product to retrieve.

    Returns:
        JSON response containing the product data with status 200 if found.
        Otherwise, returns a 404 response with a 'Product not found' message.
    """
    product = get_product_service(id)
    if product is None:
        return jsonify({"message": "Product not found"}), 404
    return jsonify(product.to_dict()), 200


def update_product(id): 
    """
    Update an existing product by its ID.

    Accepts a partial JSON payload with only the fields to update.
    Required fields from creation (e.g., name, price, quantity) are NOT required here.

    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the product to update.
      - in: body
        name: body
        required: true
        schema:
          id: ProductUpdate
          type: object
          properties:
            name:
              type: string
            price:
              type: number
            quantity:
              type: integer
            category:
              type: string
    responses:
      200:
        description: Product updated successfully
      400:
        description: Validation error
      404:
        description: Product not found
    """
    data = request.get_json()

    valid_data, errors = validate_input(ProductSchema, data, partial=True)
    if errors:
        return jsonify({"errors": errors}), 400

    product = update_product_service(id, valid_data)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    return jsonify(product.to_dict()), 200


def delete_product(id):
    """
    ---
    Controller to delete a product by its ID.

    Args:
        id (int): The ID of the product to delete.

    Returns:
        JSON response with the deleted product data and status 200 on success.
        If product not found, returns status 404 with an error message.
    """
    product = delete_product_service(id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    return jsonify(product.to_dict()), 200


def total_value():
    """
    Calculate the total inventory value (sum of price * quantity for all products).
    ---
    tags:
      - Products
    responses:
      200:
        description: Total inventory value calculated successfully
        schema:
          type: number
          format: float
          example: 25430.75
    """
    return jsonify(total_value_service()), 200



def avg_product_price():
    """
    Return the average price of all products.
    ---
    tags:
      - Products
    responses:
      200:
        description: Average product price calculated successfully
        schema:
          type: number
          format: float
          example: 123.45
    """
    return jsonify(avg_product_price_service()), 200


def min_max_price():
    """
    Return the minimum and maximum product prices.
    ---
    tags:
      - Products
    responses:
      200:
        description: Minimum and maximum product prices retrieved successfully
        schema:
          type: object
          properties:
            min_price:
              type: number
              format: float
              example: 10.99
            max_price:
              type: number
              format: float
              example: 999.99
    """
    return jsonify(min_max_price_service()), 200


def total_nb_of_products_category():
    """
    Return the count of products per category.
    ---
    tags:
      - Products
    responses:
      200:
        description: Total number of products per category retrieved successfully
        schema:
          type: array
          items:
            type: object
            properties:
              category:
                type: string
                example: "Electronics"
              total_products:
                type: integer
                example: 42
    """
    return jsonify(total_nb_of_products_category_service()), 200


def out_of_stock():
    """
    Return a list of products that are out of stock.
    ---
    tags:
      - Products
    responses:
      200:
        description: List of out of stock products retrieved successfully
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 10
              name:
                type: string
                example: "USB Cable"
              quantity:
                type: integer
                example: 0
              price:
                type: number
                format: float
                example: 9.99
              category:
                type: string
                example: "Accessories"
    """
    return jsonify(out_of_stock_service()), 200


def most_expensive_products():
    """
    Return the top 5 most expensive products.
    ---
    tags:
      - Products
    responses:
      200:
        description: Top 5 most expensive products retrieved successfully
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 3
              name:
                type: string
                example: "MacBook Pro"
              quantity:
                type: integer
                example: 7
              price:
                type: number
                format: float
                example: 2499.99
              category:
                type: string
                example: "Electronics"
    """
    return jsonify(most_expensive_products_service()), 200


def value_per_category():
    """
    Return the total value of products grouped by category.
    ---
    tags:
      - Products
    responses:
      200:
        description: Total inventory value per category retrieved successfully
        schema:
          type: array
          items:
            type: object
            properties:
              category:
                type: string
                example: "Electronics"
              total_value:
                type: number
                format: float
                example: 123456.78
    """
    return jsonify(value_per_category_service()), 200


def classify_batch():
    """
    Classify a batch of products by ID using Amazon Bedrock
    ---
    tags:
      - Classification
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              product_ids:
                type: array
                items:
                  type: integer
                example: [1, 2, 3]
    responses:
      200:
        description: Successfully classified products
        schema:
          type: object
          properties:
            updated_products:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  category:
                    type: string
                    example: "Electronics"
      400:
        description: Validation error in request payload
        schema:
          type: object
          example:
            product_ids: ["Missing data for required field."]
      404:
        description: Some product IDs were not found
        schema:
          type: object
          example:
            error: "Some product IDs not found"
    """
    try:
        data = BatchIDsSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    product_ids = data['product_ids']
    updated = classify_batch_service(product_ids)

    if updated is None:
        return jsonify({"error": "Some product IDs not found"}), 404

    updated_dicts = [product.to_dict() for product in updated]

    return jsonify({"updated_products": updated_dicts}), 200


def health_status():
    """
    Get health status of the service
    ---
    tags:
      - Health
    responses:
      200:
        description: Service is healthy
        schema:
          type: object
          properties:
            status:
              type: string
              example: ok
    """
    return health_status_service(), 200


def translate_name_description():
    """
    Translate product names and descriptions to Arabic and update the database.

    ---
    tags:
      - Products
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            product_ids:
              type: array
              items:
                type: integer
              example: [1, 2, 3]
              description: List of product IDs to translate
          required:
            - product_ids
    responses:
      200:
        description: Successfully translated and updated products
        schema:
          type: object
          properties:
            updated_products:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  arabic_name:
                    type: string
                    description: Arabic translation of product name
                  arabic_description:
                    type: string
                    description: Arabic translation of product description
      400:
        description: Validation error or bad request
      404:
        description: Some product IDs not found
      500:
        description: Internal server error
    """
    try:
        data = BatchIDsSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    product_ids = data['product_ids']
    updated = translate_name_description_service(product_ids)

    if updated is None:
        return jsonify({"error": "Some product IDs not found"}), 404

    updated_dicts = [product.to_dict() for product in updated]

    return jsonify({"updated_products": updated_dicts}), 200


def generate_embedding():
    """
    Generate vector embeddings for product names and update the database.

    ---
    tags:
      - Products
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            product_ids:
              type: array
              items:
                type: integer
              example: [1, 2, 3]
              description: List of product IDs to generate embeddings for
          required:
            - product_ids
    responses:
      200:
        description: Successfully generated and updated embeddings
        schema:
          type: object
          properties:
            updated_products:
              type: array
              items:
                type: object
                properties:
                  embedding:
                    type: array
                    items:
                      type: number
                    description: Vector embedding for the product name
      400:
        description: Validation error or bad request
      404:
        description: Some product IDs not found
      500:
        description: Internal server error
    """
    try:
        data = BatchIDsSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    product_ids = data['product_ids']
    updated = generate_embedding_service(product_ids)

    if updated is None:
        return jsonify({"error": "Some product IDs not found"}), 4
    
    return jsonify({"updated_products": updated}), 200

#Similarity Search
def similarity_search_by_id(id):
    """
    Get similar products based on embeddings
    ---
    tags:
      - Products
    summary: Get similar products
    description: Returns a list of similar products based on vector similarity using product embeddings.
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the product to find similar products for
      - name: limit
        in: query
        type: integer
        required: false
        default: 5
        description: Number of similar products to return
    responses:
      200:
        description: A list of similar products
        schema:
          type: object
          properties:
            similar_products:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  similarity_score:
                    type: number
      404:
        description: Product not found or missing embedding
        schema:
          type: object
          properties:
            error:
              type: string
    """
    limit = request.args.get("limit", 5, type=int)
    results = similarity_search_by_id_service(id, limit)
    if results is None:
        return jsonify({"error": "Product not found or missing embedding"}), 404
    return jsonify({"similar_products": results})


def similarity_search_by_name():
    """
    Search for products similar to the given name using text embeddings.

    ---
    tags:
      - Products
    parameters:
      - name: name
        in: query
        type: string
        required: true
        description: The name or phrase to find similar products for.
      - name: limit
        in: query
        type: integer
        required: false
        default: 5
        description: Maximum number of similar products to return.
    responses:
      200:
        description: A list of similar products found.
        schema:
          type: object
          properties:
            similar_products:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: Product ID
                  name:
                    type: string
                    description: Product name
      400:
        description: Missing or invalid query parameters.
        schema:
          type: object
          properties:
            error:
              type: string
      404:
        description: No similar products found or product missing embedding.
        schema:
          type: object
          properties:
            error:
              type: string
    """
    name = request.args.get("name")
    limit = request.args.get("limit", 5, type=int)

    if not name:
        return jsonify({"error": "Missing 'name' query parameter"}), 400

    results = similarity_search_by_name_service(name, limit)

    if not results:
        return jsonify({"error": "Product not found or missing embedding"}), 404

    return jsonify({"similar_products": results})