from src import db
from sqlalchemy.dialects.postgresql import JSONB


class UserDefaults(db.Model):

    __tablename__ = "user_defaults"

    phone_id = db.Column(db.String(20), primary_key=True)
    diet_preferences = db.Column(JSONB)
    diet_restrictions = db.Column(JSONB)
    cooking_appliances = db.Column(JSONB)
    utensils = db.Column(JSONB)
    location = db.Column(db.String(256))
    created_on = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, phone_id, created_on, updated_on, 
                 diet_preferences=[], diet_restrictions=[],
                 cooking_appliances=[], utensils=[], location=""):
        self.phone_id = phone_id
        self.diet_preferences = diet_preferences
        self.diet_restrictions = diet_restrictions
        self.cooking_appliances = cooking_appliances
        self.utensils = utensils
        self.location = location
        self.created_on = created_on
        self.updated_on = updated_on
        

    def __repr__(self):
        res = f"Phone_id: {self.phone_id}"
        if self.diet_preferences:
            res += f"\nDiet_preferences: {self.diet_preferences}"
        if self.diet_restrictions:
            res += f"\nDiet_restrictions: {self.diet_restrictions}"
        if self.cooking_appliances:
            res += f"\nCooking_appliances: {self.cooking_appliances}"
        if self.utensils:
            res += f"\nUtensils: {self.utensils}"
        if self.location:
            res += f"\nLocation: {self.location}"
        
        readable_created_on = self.created_on.strftime("%B %d, %Y %I:%M %p")
        readable_updated_on = self.updated_on.strftime("%B %d, %Y %I:%M %p")

        res += f"\nCreated on: {readable_created_on}"
        res += f"\nUpdated on: {readable_updated_on}"
        return res