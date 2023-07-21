from flask import Blueprint, request, jsonify
from src import db

from ResponseChat import ResponseChat, Menu, ButtonObject
import logging
import json
import openai

from src.food_update.views import handle_request as food_update_handle_request
from src.food_inventory.views import handle_request as food_inventory_handle_request
from src.main_menu.views import handle_request as main_menu_handle_request
from src.utils import get_buttons_from_data, display_main_menu

core_bp = Blueprint("core", __name__)

@core_bp.route('/', methods=['POST'])
def handle_request():
    r = ResponseChat()
    logging.basicConfig(filename='chat_builder.log', level=logging.INFO)
    logging.info('##################Food manager Request#####################')

    json_data = request.get_json()
    logging.info('Data: {}'.format(json.dumps(json_data)))

    # possible bot_states:
    bot_states_dict = {
        "Main_Menu": main_menu_handle_request,
        "Food_Inventory_Menu": food_inventory_handle_request,
        "Food_Update_Menu": "Food_Update_Menu",
        "Past_Meals_Menu": "Past_Meals_Menu",
        "Meal_Suggestions_Menu": "Meal_Suggestions_Menu",
        "Favorite_Meals_Menu": "Favorite_Meals_Menu",
        "Meal_Recording_Menu": "Meal_Recording_Menu",
        "User_Preferences_Menu": "User_Preferences_Menu"
    }

    bot_state_handler = bot_states_dict.get(json_data["bot_state"], None)

    if bot_state_handler:
        bot_state_handler(r, json_data, logging)
    elif json_data["data"]["type"] == "text":
        display_main_menu(r)      
    else:
        r.send_text("Invalid Request data")

    logging.info('Return: {}'.format(r.get_data()))
    return jsonify(r.get_response())
