import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
env_config = f"config.{os.getenv('ENV')}Config"
app.config.from_object(env_config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from src.core.views import core_bp
from src.food_inventory.views import food_inventory_bp


app.register_blueprint(core_bp)
app.register_blueprint(food_inventory_bp)

from src.food_inventory.models import FoodInventory

if __name__ == '__main__':
    # Create the database tables
    db.create_all()

    # Run the Flask app
    app.run(debug=True)
