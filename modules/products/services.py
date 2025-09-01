from sqlalchemy import func, or_, text
from aws_translate_service.translate import translate
from bedrock.embedding_generator import invoke_bedrock_embedding
from modules.products.model import Products
from modules.products.extension import db
from bedrock.category_classifier import invoke_bedrock_category
#CRUD

#CREATE product
def add_product_service(data):
    """
    Create a new product record in the database.
    ---
    tags:
      - Products
    parameters:
      - name: data
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: "Wireless Headphones"
            price:
              type: number
              format: float
              example: 199.99
            quantity:
              type: integer
              example: 50
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
              example: 101
            name:
              type: string
              example: "Wireless Headphones"
            price:
              type: number
              example: 199.99
            quantity:
              type: integer
              example: 50
            category:
              type: string
              example: "Electronics"
            in_stock:
              type: boolean
              example: true
      400:
        description: Validation error
    """
    if not data.get("category"):
        product_name = data.get("name")
        if product_name:
            category = invoke_bedrock_category(product_name)
            data["category"] = category
        else:
            data["category"] = "Uncategorized"

    new_product = Products(**data)
    new_product.in_stock = new_product.quantity > 0
    db.session.add(new_product)
    db.session.commit()
    return new_product


#READ
#all products
def get_products_service():
    """
    Retrieve all products from the database.
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
                example: "Wireless Mouse"
              category:
                type: string
                example: "Electronics"
              price:
                type: number
                format: float
                example: 25.99
              quantity:
                type: integer
                example: 100
              in_stock:
                type: boolean
                example: true
    """
    return Products.query.all()


#particular product
def get_product_service(id):
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
              example: "Wireless Mouse"
            category:
              type: string
              example: "Electronics"
            price:
              type: number
              format: float
              example: 25.99
            quantity:
              type: integer
              example: 100
            in_stock:
              type: boolean
              example: true
      404:
        description: Product not found
    """
    product = Products.query.get(id)
    if not product:
        return None
    return product


#UPDATE product
def update_product_service(id, data):
    """
    Update an existing product's attributes based on provided data.
    ---
    Args:
        id (int): The unique identifier of the product to update.
        data (dict): A dictionary containing the product attributes to update.

    Returns:
        Products or None: The updated product instance if found; otherwise, None.
    """
    product = Products.query.get(id)
    if not product:
        return None
    
    for key, value in data.items():
        setattr(product, key, value)

    if 'quantity' in data:
        product.in_stock = product.quantity > 0

    db.session.commit()

    return product


#DELETE product
def delete_product_service(id):
    """
    Delete a product from the database by its ID.
    ---
    Args:
        id (int): The unique identifier of the product to delete.

    Returns:
        Products or None: The deleted product instance if found; otherwise, None.
    """
    product = Products.query.get(id)
    if not product:
        return None
    db.session.delete(product)
    db.session.commit()

    return product


#Additional calls

#Total inventory value
def total_value_service():
    """
    Calculate the total inventory value by summing the product of price and quantity for all products.
    ---
    Returns:
        float: The total value of all products in inventory. Returns 0 if no products exist.
    """
    return db.session.query(func.sum(Products.price * Products.quantity)).scalar() or 0


#average product price
def avg_product_price_service():
    """
    Calculate the average price of all products.
    ---
    Returns:
        float: The average price of products. Returns 0 if no products exist.
    """
    return db.session.query(func.avg(Products.price)).scalar() or 0


#max/min price
def min_max_price_service():
    """
    Retrieve the minimum and maximum product prices.
    ---
    Returns:
        tuple: A tuple containing (max_price, min_price).
               Both values are floats. Returns (0, 0) if no products exist.
    """
    min_price = db.session.query(func.min(Products.price)).scalar() or 0
    max_price = db.session.query(func.max(Products.price)).scalar() or 0
    return (max_price, min_price)


#total number of products per category
def total_nb_of_products_category_service():
    """
    Count the total number of products grouped by category.
    ---
    Returns:
        list of dict: Each dictionary contains 'category' (str) and 'count' (int) keys,
                      representing the category name and the number of products in that category.
    """
    results = db.session.query(Products.category, func.count(Products.id)).group_by(Products.category).all()
    return [{"category": category, "count": count} for category, count in results]


#out-of-stock products
def out_of_stock_service():
    """
    Retrieve all products that are out of stock.
    ---
    A product is considered out of stock if its quantity is zero or its in_stock flag is False.

    Returns:
        list of dict: A list of products represented as dictionaries that are currently out of stock.
    """
    results = Products.query.filter(or_(Products.quantity == 0, Products.in_stock == False)).all()
    return [product.to_dict() for product in results]


#5 most expensive items
def most_expensive_products_service():
    """
    Retrieve the top 5 most expensive products.
    ---
    Products are ordered by price in descending order and limited to the first 5 entries.

    Returns:
        list of dict: A list of up to 5 products represented as dictionaries with the highest prices.
    """
    results = Products.query.order_by(Products.price.desc()).limit(5)
    return [product.to_dict() for product in results]


#total value per category
def value_per_category_service():
    """
    Calculate the total value of products grouped by category.
    ---
    The total value for each category is the sum of (quantity * price) of all products in that category.

    Returns:
        list of dict: A list of dictionaries where each dictionary contains:
            - "category" (str): The product category.
            - "sum" (float): The total value of products in that category.
    """
    results = db.session.query(Products.category,func.sum(Products.quantity * Products.price)).group_by(Products.category)
    return [{"category": category, "sum": sum} for category, sum in results]

#batch classifying
def classify_batch_service(product_ids):
    """
    Classify a batch of products using Amazon Bedrock based on their names.
    ---
    tags:
      - Classification
    parameters:
      - name: product_ids
        in: body
        required: true
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
        description: Categories assigned successfully
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
    products = Products.query.filter(Products.id.in_(product_ids)).all()
    if len(products) != len(product_ids):
        return None

    updated_products = []
    for product in products:
        category = invoke_bedrock_category(product.name)
        product.category = category
        updated_products.append({'id': product.id, 'category': category})

    db.session.commit()
    return updated_products


#health check
def health_status_service():
    """
    Health check service returning status OK.
    ---
    tags:
      - Health
    responses:
      200:
        description: Service is up and running
        schema:
          type: object
          properties:
            status:
              type: string
              example: "ok"
    """
    return {"status": "ok"}

#batch product name/description translation
def translate_name_description_service(products_ids):
    """
    Translate the name and description of multiple products to Arabic and update them in the database.

    ---
    tags:
      - Products
    parameters:
      - in: body
        name: products_ids
        description: List of product IDs to translate
        required: true
        schema:
          type: array
          items:
            type: integer
          example: [1, 2, 3]
    responses:
      200:
        description: Products successfully translated and updated
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: Product ID
              arabic_name:
                type: string
                description: Translated Arabic name
              arabic_description:
                type: string
                description: Translated Arabic description
      400:
        description: Some product IDs not found or invalid input
      500:
        description: Internal server error
    """
    products = Products.query.filter(Products.id.in_(products_ids)).all()
    if len(products) != len(products_ids):
        return None  # You can customize this error handling
    
    for product in products:
        product.arabic_name = translate(product.name)
        product.arabic_description = translate(product.description)

    db.session.commit()
    return products


#generate embeddings
def generate_embedding_service(product_ids):
    """
    Generate vector embeddings for the names of multiple products and update them in the database.

    ---
    tags:
      - Products
    parameters:
      - in: body
        name: product_ids
        description: List of product IDs to generate embeddings for
        required: true
        schema:
          type: array
          items:
            type: integer
          example: [1, 2, 3]
    responses:
      200:
        description: Embeddings successfully generated and stored
        schema:
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
        description: Some product IDs not found or invalid input
      500:
        description: Internal server error
    """
    products = Products.query.filter(Products.id.in_(product_ids)).all()
    if len(products) != len(product_ids):
        return None

    updated_products = []
    for product in products:
        embedding = invoke_bedrock_embedding(product.name)
        product.embedding = embedding
        updated_products.append({'embedding': embedding})

    db.session.commit()
    return updated_products


def similarity_search_by_id_service(id, limit=5):
    """
    Perform similarity search for a given product based on its embedding.

    ---
    tags:
      - Products
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the target product to compare against
      - name: limit
        in: query
        type: integer
        required: false
        default: 5
        description: Number of similar products to return
    responses:
      200:
        description: List of similar products
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: ID of the similar product
              name:
                type: string
                description: Name of the similar product
      404:
        description: Product not found or no embedding available
    """
    product = Products.query.get(id)
    if not product or product.embedding is None:
        return None

    target_embedding = product.embedding.tolist()
    # Convert list to PostgreSQL vector literal string
    vector_literal = f"'[{','.join(map(str, target_embedding))}]'::vector({len(target_embedding)})"


    query = text(f"""
                 SELECT id, name, embedding, embedding <#> {vector_literal} AS similarity
                 FROM inventory.products
                 WHERE id != :target_id
                 ORDER BY similarity
                 LIMIT :limit
                 """)


    results = db.session.execute(
        query,
        {
            "target_id": id,
            "limit": limit
        }
    )

    return [{"id": row.id, "name": row.name} for row in results]


def similarity_search_by_name_service(name, limit=5):
    """
    Generate an embedding for the given name and perform similarity search in the product database.

    ---
    parameters:
      - name: name
        in: body
        type: string
        required: true
        description: The name or phrase to generate embeddings for and search similar products.
      - name: limit
        in: body
        type: integer
        required: false
        default: 5
        description: Number of similar products to return.

    returns:
      type: list
      items:
        type: object
        properties:
          id:
            type: integer
            description: Product ID
          name:
            type: string
            description: Product name
    """
    target_embedding = invoke_bedrock_embedding(name)

    vector_literal = f"'[{','.join(map(str, target_embedding))}]'::vector({len(target_embedding)})"

    query = text(f"""
                 SELECT id, name, embedding <#> {vector_literal} AS similarity
                 FROM inventory.products
                 WHERE embedding IS NOT NULL
                 ORDER BY similarity
                 LIMIT :limit
                 """)

    results = db.session.execute(
        query,
        {
            "limit": limit
        }
    )
    return [{"id": row.id, "name": row.name} for row in results]