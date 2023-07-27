from src import db


class FoodInventory(db.Model):

    __tablename__ = "food_inventory"

    id = db.Column(db.Integer, primary_key=True)
    phone_id = db.Column(db.String(20))
    name = db.Column(db.String(256))
    quantity = db.Column(db.Integer)
    units = db.Column(db.String(25))
    category = db.Column(db.String(256))
    sub_category = db.Column(db.String(256))
    created_on = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float)

    def __init__(self, phone_id, name, quantity, units, category, created_on, updated_on, sub_category=None, price=None):
        self.phone_id = phone_id
        self.name = name
        self.quantity = quantity
        self.units = units
        self.category = category
        self.sub_category = sub_category
        self.price = price
        self.created_on = created_on
        self.updated_on = updated_on

    def __repr__(self):
        res = f"Item: {self.name}\nQuantity: {self.quantity} {self.units}\nCategory: {self.category}"
        if self.sub_category:
            res += f" ({self.sub_category})"
        if self.price:
            res += f"\n{self.price}"
        readable_updated_on = self.updated_on.strftime("%B %d, %Y %I:%M:%S %p")
        res += f"\nUpdated on: {readable_updated_on}"
        return res
