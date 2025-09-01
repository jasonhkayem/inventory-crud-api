from flask import Flask
from flask_cors import CORS
from modules.products.extension import db, ma, swagger
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)  # This enables CORS for all routes and origins by default

# Initialize extensions
db.init_app(app)
ma.init_app(app)
swagger.init_app(app)

# Register blueprints
from modules.products.routes import products_bp
app.register_blueprint(products_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)