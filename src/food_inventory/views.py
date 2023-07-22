from flask import Blueprint, request, jsonify
from ResponseChat import ResponseChat
from src.utils import display_main_menu, get_buttons_from_data, display_food_inventory
import logging
import json
from src.db_utils import is_food_inventory_empty, add_to_food_inventory, fetch_food_inventory_categories, fetch_food_inventory_by_category

food_inventory_bp = Blueprint("food_inventory", __name__)

# Food inventory menu
@food_inventory_bp.route('/food_inventory', methods=['POST'])
def handle_request(r=None, json_data=None, logging=None):
    do_return = False
        
    if not r:
        r = ResponseChat()
    if not json_data:
        json_data = request.get_json()
        import logging
        logging.basicConfig(filename='chat_builder.log', level=logging.INFO)
        do_return = True

    logging.info('Data: {}'.format(json.dumps(json_data)))

    # add to food inventory if needed
    if (json_data["data"]["type"] == "add_data"):
        init = json_data["data"].get("init", False)
        if init:
            r.send_text("Clearing existing data in Food inventory")
        add_to_food_inventory(phone_id, init)
        r.send_text("Sample stock added in Food inventory")

    elif (json_data["data"]["type"] == "reply"):
        reply_id = json_data["data"]["body"]["id"]
        title = json_data["data"]["body"]["title"]
        if reply_id != "Main_Menu":
            # show data
            query_result = fetch_food_inventory_by_category(phone_id, title)
            ls = [repr(row) for row in query_result]
            r.send_list(ls)
            display_food_inventory(r)
        else:
            display_main_menu(r)
    else:
        # todo: add interaction with chatgpt here
        display_food_inventory(r)

    if do_return:
        logging.info('Return: {}'.format(r.get_data()))
        return jsonify(r.get_response())