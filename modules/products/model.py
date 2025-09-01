from datetime import datetime
from .extension import db
from pgvector.sqlalchemy import Vector

class Products(db.Model):
    """
    Represents a product in the inventory.

    Attributes:
        id (int): Primary key, unique product identifier.
        name (str): Name of the product.
        category (str): Category the product belongs to.
        price (Decimal): Price of the product with 2 decimal precision.
        quantity (int): Available quantity in stock.
        in_stock (bool): Indicates if the product is in stock (True if quantity > 0).
        created_at (datetime): Timestamp when the product was created.

    Methods:
        to_dict(): Returns a dictionary representation of the product, 
                   suitable for JSON serialization.
    """
    __tablename__ = 'products'
    __table_args__ = {'schema': 'inventory'}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    in_stock = db.Column(db.Boolean, nullable=False, default=True)
    embedding = db.Column(Vector(1024))
    created_at = db.Column(db.DateTime, default=datetime.now)
    arabic_name = db.Column(db.String(100))
    arabic_description = db.Column(db.String())

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'price': float(self.price),
            'quantity': self.quantity,
            'in_stock': self.in_stock,
            'embedding': self.embedding.tolist() if self.embedding is not None else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'arabic_name': self.arabic_name,
            'arabic_description': self.arabic_description
        }

