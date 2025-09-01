from flask import Blueprint, request

from .controller import(
    add_product,
    generate_embedding,
    get_products,
    get_product,
    health_status,
    similarity_search_by_id,
    similarity_search_by_name,
    translate_name_description,
    update_product,
    delete_product,
    total_value,
    total_nb_of_products_category,
    avg_product_price,
    min_max_price,
    value_per_category,
    most_expensive_products,
    out_of_stock,
    classify_batch
)

products_bp = Blueprint('products', __name__)

#CRUD

# CREATE Product
@products_bp.route('/products', methods=['POST'])
def create_product_route():
    """
    Create a new product.
    ---
    tags:
      - Products
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
                example: "iPhone 13"
              quantity:
                type: integer
                example: 10
              price:
                type: number
                format: float
                example: 999.99
              category:
                type: string
                example: "Electronics"
    responses:
      201:
        description: Product created successfully
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: "iPhone 13"
            quantity:
              type: integer
              example: 10
            price:
              type: number
              example: 999.99
            category:
              type: string
              example: "Electronics"
      400:
        description: Validation error
    """
    return add_product()


# READ Product(s)
# List all products
@products_bp.route('/products', methods=['GET'])
def get_products_route():
    """
    Retrieve a list of all products.
    ---
    tags:
      - Products
    responses:
      200:
        description: A list of all products
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              name:
                type: string
                example: "MacBook Air"
              quantity:
                type: integer
                example: 5
              price:
                type: number
                format: float
                example: 1299.99
              category:
                type: string
                example: "Electronics"
    """
    return get_products()


# Fetch single product by ID
@products_bp.route('/products/<int:id>', methods=['GET'])
def get_product_route(id):
    """
    Retrieve a single product by its ID.
    ---
    tags:
      - Products
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the product to retrieve
    responses:
      200:
        description: Product retrieved successfully
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: "AirPods Pro"
            quantity:
              type: integer
              example: 12
            price:
              type: number
              format: float
              example: 249.99
            category:
              type: string
              example: "Electronics"
      404:
        description: Product not found
    """
    return get_product(id)


# UPDATE Product by ID
@products_bp.route('/products/<int:id>', methods=['PUT'])
def update_product_route(id):
    """
    Update an existing product identified by its ID.
    ---
    tags:
      - Products
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the product to update
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
                example: "MacBook Pro"
              quantity:
                type: integer
                example: 8
              price:
                type: number
                format: float
                example: 1999.99
              category:
                type: string
                example: "Electronics"
    responses:
      200:
        description: Product updated successfully
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: "MacBook Pro"
            quantity:
              type: integer
              example: 8
            price:
              type: number
              example: 1999.99
            category:
              type: string
              example: "Electronics"
      400:
        description: Validation error
      404:
        description: Product not found
    """
    return update_product(id)


# DELETE Product by ID
@products_bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product_route(id):
    """
    Delete a product by its ID.
    ---
    tags:
      - Products
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the product to delete
    responses:
      200:
        description: Product deleted successfully
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: "MacBook Pro"
            quantity:
              type: integer
              example: 8
            price:
              type: number
              example: 1999.99
            category:
              type: string
              example: "Electronics"
      404:
        description: Product not found
    """
    return delete_product(id)


# Total Inventory Value
@products_bp.route('/products/total_value', methods=['GET'])
def total_value_route():
    """
    Calculate the total inventory value.
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
    return total_value()


# Average Product Price
@products_bp.route('/products/avg_product_price', methods=['GET'])
def avg_product_price_route():
    """
    Calculate the average price of all products.
    ---
    tags:
      - Products
    responses:
      200:
        description: Average product price calculated successfully
        schema:
          type: number
          format: float
          example: 349.99
    """
    return avg_product_price()


# Minimum/Maximum Price
@products_bp.route('/products/min_max_price', methods=['GET'])
def min_max_price_route():
    """
    Retrieve the minimum and maximum product prices.
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
              example: 9.99
            max_price:
              type: number
              format: float
              example: 1999.99
    """
    return min_max_price()


# Total Number of Products per Category
@products_bp.route('/products/total_products_per_category', methods=['GET'])
def total_nb_products_category_route():
    """
    Retrieve total count of products grouped by category.
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
    return total_nb_of_products_category()


# Out-of-Stock Products
@products_bp.route('/products/out_of_stock', methods=['GET'])
def out_of_stock_route():
    """
    Retrieve a list of products that are out of stock.
    ---
    tags:
      - Products
    responses:
      200:
        description: List of out of stock products
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
    return out_of_stock()


# 5 Most Expensive Items
@products_bp.route('/products/most_expensive', methods=['GET'])
def most_expensive_products_route():
    """
    Retrieve the top 5 most expensive products.
    ---
    tags:
      - Products
    responses:
      200:
        description: List of top 5 most expensive products
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
    return most_expensive_products()


# Value per Category
@products_bp.route('/products/value_per_category', methods=['GET'])
def value_per_category_route():
    """
    Calculate the total inventory value per product category.
    ---
    tags:
      - Products
    responses:
      200:
        description: Total inventory value per category
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
    return value_per_category()


#Batch classifying
@products_bp.route("/products/classify_batch", methods=['PUT'])
def classify_batch_route():
    """
    Classify a batch of products based on their names using Amazon Bedrock
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
        description: One or more product IDs were not found
    """
    return classify_batch()


#health
@products_bp.route("/health", methods=["GET"])
def health_status_route():
    """
    Health check endpoint
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
    return health_status()

#batch name/description translation
@products_bp.route("/products/translate", methods=['PUT'])
def translate_name_description_route():
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
                    description: Arabic translation of the product name
                  arabic_description:
                    type: string
                    description: Arabic translation of the product description
      400:
        description: Validation error or bad request
      404:
        description: Some product IDs not found
      500:
        description: Internal server error
    """
    return translate_name_description()


#generate embeddings
@products_bp.route("/products/embedding", methods=['PUT'])
def generate_embedding_route():
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
        description: Successfully generated and stored embeddings
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
                    description: The vector embedding for the product name
      400:
        description: Validation error or bad request
      404:
        description: Some product IDs not found
      500:
        description: Internal server error
    """
    return generate_embedding()


#Similarity search
@products_bp.route("/products/similarity_by_id/<int:id>", methods=["GET"])
def similarity_search_by_id_route(id):
    """
    Find similar products by embedding similarity.

    ---
    tags:
      - Products
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
        description: Maximum number of similar products to return
    responses:
      200:
        description: List of similar products
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
      404:
        description: Product not found or missing embedding
        schema:
          type: object
          properties:
            error:
              type: string
    """
    return similarity_search_by_id(id)

@products_bp.route("/products/similarity_by_name", methods=['GET'])
def similarity_search_by_name_route():
    """
    Similarity search by product name endpoint.

    ---
    get:
      summary: Find products similar to the given name using embeddings.
      tags:
        - Products
      parameters:
        - name: name
          in: query
          required: true
          schema:
            type: string
          description: Name or phrase to search for similar products.
        - name: limit
          in: query
          required: false
          schema:
            type: integer
            default: 5
          description: Number of similar products to return.
      responses:
        200:
          description: List of similar products.
          content:
            application/json:
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
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
        404:
          description: No similar products found or missing embeddings.
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
    """
    return similarity_search_by_name()