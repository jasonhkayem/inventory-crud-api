from marshmallow import Schema, fields, validate

class ProductSchema(Schema):
    """
    Marshmallow schema for validating and deserializing Product data.
    ---
    definitions:
      Product:
        type: object
        properties:
          name:
            type: string
            minLength: 2
            maxLength: 100
          category:
            type: string
            minLength: 1
            nullable: true
          description:
            type: string
          price:
            type: number
            minimum: 1
            format: float
          quantity:
            type: integer
          in_stock:
            type: boolean
          embedding:
            type: array
            items:
              type: number
              format: float
          arabic_name:
            type: string
            nullable: true
          arabic_description:
            type: string
            nullable: true
        required:
          - name
          - description
          - price
          - quantity
    """
    name = fields.String(required=True, validate=validate.Length(min=2, max=100))
    category = fields.String(required=False, allow_none=True, load_default=None, validate=validate.Length(min=1))
    description = fields.String(required=True)
    price = fields.Float(required=True, validate=validate.Range(min=1))
    quantity = fields.Integer(required=True)
    in_stock = fields.Bool(required=False)
    embedding = fields.List(fields.Float(), required=False, allow_none=True, load_default=None)
    arabic_name = fields.String(required=False)
    arabic_description = fields.String(required=False)


class BatchIDsSchema(Schema):
    product_ids = fields.List(fields.Int(), required=True)