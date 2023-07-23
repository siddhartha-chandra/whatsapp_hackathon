from src import db
from datetime import datetime
from src.food_inventory.models import FoodInventory
from src.user_defaults.models import UserDefaults
from src.conversations.models import Conversations
from sqlalchemy.orm.session import make_transient

def columns(table_obj):
    return table_obj.columns

### Food Inventory ###
def update_food_inventory_item(phone_id, name, item_dict):

    to_update = fetch_food_inventory_by_name(phone_id, name)
    item_dict['created_on'] = datetime.now()
    item_dict['updated_on'] = datetime.now()
    
    if to_update:
        item_dict['created_on'] = to_update.created_on
        delete_from_food_inventory(phone_id, name)
        make_transient(to_update)
       
    record = FoodInventory(**item_dict)
    db.session.add(record)
    db.session.commit()

def delete_from_food_inventory(phone_id, name):
    db.session.query(FoodInventory).filter_by(phone_id=phone_id, name=name).delete()
    db.session.commit()

def get_food_inventory_columns():
    return columns(FoodInventory)

def fetch_food_inventory_categories():
    res = db.session.query(FoodInventory.category).distinct().all()
    res = [item[0] for item in res]
    return res

def fetch_food_inventory_subcategories():
    res = db.session.query(FoodInventory.sub_category).distinct().all()
    res = [item[0] for item in res if res]
    return res

def fetch_food_inventory_by_name(phone_id, name):
    return db.session.query(FoodInventory).filter_by(phone_id=phone_id, name=name).first()

def fetch_food_inventory_by_category(phone_id, category):
    return db.session.query(FoodInventory).filter_by(phone_id=phone_id, category=category).all()

def fetch_food_inventory_for_user(phone_id):
    return db.session.query(FoodInventory).filter_by(phone_id=phone_id).all()

def is_food_inventory_empty(phone_id):
    return len(fetch_food_inventory_for_user(phone_id)) == 0

def add_to_food_inventory(phone_id, init=False):
    # drop all items in the table 'food_inventory'
    if init:
        db.session.query(FoodInventory).delete()

    phone_id = phone_id
    created_on = datetime.now()
    updated_on = datetime.now()

    ls = [
        dict(name="rolled oats", quantity=500, units="grams", category="cereal"),
        dict(name="blueberries", quantity=100, units="grams", category="fruits", sub_category="berries"),
        dict(name="carrots", quantity=1, units="kilograms", category="vegetables"),
        dict(name="medium Avocado", quantity=8, units="pieces", category="fruits"),
        dict(name="quinoa", quantity=500, units="grams", category="grains"),
        dict(name="peanut butter", quantity=500, units="grams", category="nuts", sub_category="butter"),
        dict(name="tomato", quantity=500, units="grams", category="vegetables"),
        dict(name="almond Butter", quantity=250, units="grams", category="nuts", sub_category="butter"),
        dict(name="mint leaves", quantity=200, units="grams", category="herbs"),
        dict(name="small Lemon", quantity=5, units="pieces", category="fruits"),
        dict(name="salt", quantity=250, units="grams", category="seasonings"),
        dict(name="pepper", quantity=100, units="grams", category="seasonings"),
    ]

    for item in ls:
        item["phone_id"] = phone_id
        item["created_on"] = created_on
        item["updated_on"] = updated_on
        item = FoodInventory(**item)
        db.session.add(item)

    db.session.commit()


### User Defaults ###
def create_user_defaults(phone_id):
    created_on = datetime.now()
    updated_on = datetime.now()
    res = UserDefaults(phone_id=phone_id, created_on=created_on, updated_on=updated_on)
    return res

def clear_user_preferences(phone_id):
    db.session.query(UserDefaults).filter_by(phone_id=phone_id).delete()
    db.session.commit()

def update_user_preferences(phone_id, record):
    clear_user_preferences(phone_id)
    make_transient(record)
    db.session.add(record)
    db.session.commit()
    

def get_user_defaults_columns():
    return columns(UserDefaults)

def add_to_user_defaults(phone_id):
    # drop all items in the table 'user_defaults'
    db.session.query(UserDefaults).delete()

    phone_id = phone_id
    created_on = datetime.now()
    updated_on = datetime.now()
    location = "Andheri(W), Mumbai, India"
    diet_preferences = ["oil-free", "Vegan", "salt-free", "sugar free"]
    diet_restrictions = ["papaya", "peanuts"]
    cooking_appliances = ["toaster", "slow juicer", "blender"]
    utensils = ["frying pan", "wok", "medium cooking pot"]

    user_defaults = UserDefaults(
        phone_id=phone_id, 
        created_on=created_on, 
        updated_on=updated_on,
        location=location, 
        diet_preferences=diet_preferences, 
        diet_restrictions=diet_restrictions,
        cooking_appliances=cooking_appliances,
        utensils=utensils)
    
    db.session.add(user_defaults)

    db.session.commit()

def fetch_user_defaults(phone_id):
    return db.session.query(UserDefaults).filter_by(phone_id=phone_id).first()

def fetch_conversation(phone_id):
    return db.session.query(Conversations).filter_by(phone_id=phone_id).first()


### User Conversations ###
def get_conversation_columns():
    return columns(Conversations)

def clear_conversation(phone_id):
    db.session.query(Conversations).filter_by(phone_id=phone_id).delete()
    db.session.commit()

def update_user_conversation(phone_id, messages):
    conversation = fetch_conversation(phone_id)
    conversation.updated_on = datetime.now()
    conversation.messages = messages

    # overwrite data in table
    clear_conversation(phone_id)  
    make_transient(conversation)  
    db.session.add(conversation)
    db.session.commit()

def add_msg_to_conversation(phone_id, messages):
    # first fetch conversation
    conversation = fetch_conversation(phone_id)
    created_on = datetime.now()
    updated_on = datetime.now()
    if conversation:
        conversation.updated_on = updated_on
        conversation.messages = conversation.messages + messages
        clear_conversation(phone_id)
        make_transient(conversation)
    else:
        conversation = Conversations(phone_id=phone_id, created_on=created_on, updated_on=updated_on, messages=messages)

    db.session.add(conversation)
    db.session.commit()
