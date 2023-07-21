from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

username = "siddhartha"
password = "helloSq1"
hostname = "localhost"
dbname = "hackathon"

SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{username}:{password}@{hostname}/{dbname}"

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

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
