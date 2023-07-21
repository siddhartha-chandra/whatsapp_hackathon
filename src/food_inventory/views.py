from flask import Blueprint, request, jsonify
from ResponseChat import ResponseChat
from src.utils import display_main_menu, get_buttons_from_data, display_food_inventory
import logging
import json
from src.db_utils import init_food_inventory, fetch_food_inventory_categories, fetch_food_inventory_by_category

food_inventory_bp = Blueprint("food_inventory", __name__)

# Food inventory menu
@food_inventory_bp.route('/food_inventory', methods=['POST'])
def handle_request(r=None, json_data=None, logging=None):
    do_return = False
    if logging:
        logging.info('Data: {}'.format(json.dumps(json_data)))
    if not r:
        r = ResponseChat()
    if not json_data:
        json_data = request.get_json()
        logging.basicConfig(filename='chat_builder.log', level=logging.INFO)
        do_return = True

    # init food inventory if needed
    if (json_data["data"]["type"] == "initialize"):
        init_food_inventory(json_data["caller"]["id"])
        r.send_text("Food inventory initialized")

    elif (json_data["data"]["type"] == "reply"):
        reply_id = json_data["data"]["body"]["id"]
        title = json_data["data"]["body"]["title"]
        phone_id = json_data["caller"]["id"]
        if reply_id != "Main_Menu":
            # show data
            query_result = fetch_food_inventory_by_category(phone_id, title)
            ls = [repr(row) for row in query_result]
            r.send_list(ls)
        else:
            display_main_menu(r)
    else:
        display_food_inventory(r)

    if do_return:
        logging.info('Return: {}'.format(r.get_data()))
        return jsonify(r.get_response())