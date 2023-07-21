from src import db
from datetime import datetime
from src.food_inventory.models import FoodInventory


def fetch_food_inventory_categories():
    return db.session.query(FoodInventory.category).distinct().all()

def fetch_food_inventory_by_category(phone_id, category):
    return db.session.query(FoodInventory).filter_by(phone_id=phone_id, category=category).all()


def init_food_inventory(phone_id):
    # drop all items in the table 'food_inventory'
    db.session.query(FoodInventory).delete()
    phone_id = phone_id
    created_on = datetime.now()
    updated_on = datetime.now()

    ls = [
        dict(name="Rolled Oats", quantity=500, units="grams", category="Cereal"),
        dict(name="Blueberries", quantity=100, units="grams", category="Fruits", sub_category="Berries"),
        dict(name="Carrots", quantity=1, units="kilograms", category="Vegetables"),
        dict(name="Medium Avocado", quantity=8, units="pieces", category="Fruits"),
        dict(name="Quinoa", quantity=500, units="grams", category="Grains"),
        dict(name="Peanut Butter", quantity=500, units="grams", category="Nuts", sub_category="Butter"),
        dict(name="Tomato", quantity=500, units="grams", category="Vegetables"),
        dict(name="ALmond Butter", quantity=250, units="grams", category="Nuts", sub_category="Butter"),
        dict(name="Mint Leaves", quantity=200, units="grams", category="Herbs"),
        dict(name="small Lemon", quantity=5, units="pieces", category="Fruits"),
        dict(name="salt", quantity=250, units="grams", category="Seasonings"),
        dict(name="pepper", quantity=100, units="grams", category="Seasonings"),
    ]

    for item in ls:
        item["phone_id"] = phone_id
        item["created_on"] = created_on
        item["updated_on"] = updated_on
        item = FoodInventory(**item)
        db.session.add(item)

    db.session.commit()