from flask import Blueprint, request, jsonify
from ResponseChat import ResponseChat
from src.utils import display_main_menu, get_buttons_from_data, display_food_inventory
import logging
import json
from src.db_utils import (
    is_food_inventory_empty, add_to_food_inventory, fetch_food_inventory_categories, 
    fetch_food_inventory_by_category, fetch_conversation, fetch_food_inventory_by_name,
    clear_conversation, fetch_food_inventory_subcategories, add_msg_to_conversation,
    delete_from_food_inventory, update_food_inventory_item, fetch_food_inventory_units
    )
from src.llm_utils import ConversationAgent

food_inventory_bp = Blueprint("food_inventory", __name__)

def update_generate_dict(dict_, agent, item):
    inputted_units = dict_.get("units")
    if inputted_units:
        units = fetch_food_inventory_units()
        text = f"I have the following list of units: {units}. Ignoring any typos, long-forms or short-forms, if '{inputted_units}' matches any item from the list: {units}, then return JUST the matched value as response. Otherwise simply return {inputted_units} as your response"
        response = agent.generate_response(text)
        try:
            dict_["units"] = json.loads(response).get("units")
        except Exception as e:
            dict_["units"] = response
            
    # get values of category and sub-category from list provided
    if not dict_.get("category"):
        categories = fetch_food_inventory_categories()
        ## interpret the value of category
        text = f"What is the category of the following item: {item}? You can use the following categories : {categories} as a reference. If it doesn't fit any category, feel free to create a new one. Please return the asnwer in the JSON format: 'category': <category_name>"
        response = agent.generate_response(text)
        dict_["category"] = json.loads(response).get("category")
    if dict_["category"] and not dict_.get("sub_category"):
        ## optionally, interpret the value of sub_category
        sub_categories = fetch_food_inventory_subcategories()
        ## interpret the value of category
        text = f"What is the sub-category of the following item: {item}, given that it's category is {dict_['category']}? You can use the following sub_categories : {sub_categories} as a reference. If it doesn't fit any category, feel free to create a new one or leave it empty. Please return the asnwer in the JSON format: 'sub_category': <sub_category name>"
        response = agent.generate_response(text)
        response_final = json.loads(response).get("sub_category")
        if response_final:
            dict_["sub_category"] = response_final
    return dict_

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

    phone_id = json_data["caller"]["id"]

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
        if reply_id == "Main_Menu":
            display_main_menu(r)
        else:
            # show data
            query_result = fetch_food_inventory_by_category(phone_id, title)
            ls = [repr(row) for row in query_result]
            r.send_list(ls)
            display_food_inventory(r)
        
    else:
        # workflow
        # this is when user wants to add/modify item in the inventiry dataset

        # STEPS:
        # do conversation only when user data starts with 'add' or 'modify' or there is conversational context
        message_history = fetch_conversation(phone_id)
        user_response  = json_data["data"]["body"]["data"].lower()
        
        # 1. if conversation does not exist and add/modify/delete starts the request:
        if not message_history and any(user_response.startswith(s) for s in ["add", "modify", "delete"]):
            # For modify:
            if user_response.startswith("modify"):
                item = user_response[6:].strip()
                query_result = fetch_food_inventory_by_name(phone_id, item)
                if query_result:
                    text = f"""The item: {item} is present in the inventory, and has the following properties: \n{query_result}"""
                    r.send_text(text)
                    text = f"""Please enter the new values for 'quantity' and 'units'. Optionally provide the name, category and sub_category"""
                    r.send_text(text)
                    message = f"modify {item}"
                    add_msg_to_conversation(phone_id, [{"role": "user", "content": message}])
                else:
                    text = f"The item: {item} is not present in the inventory! Let's start over again"
                    clear_conversation(phone_id)
                    r.send_text(text)
                    display_food_inventory(r)
            elif user_response.startswith("delete"):
                item = user_response[7:].strip()
                query_result = fetch_food_inventory_by_name(phone_id, item)
                if query_result:
                    text = f"""The item: {item} is present in the inventory, and has the following properties: \n{query_result}"""
                    r.send_text(text)
                    text = f"""Are you sure you want to delete this item ?"""
                    r.send_text(text)
                    message = f"delete {item}"
                    add_msg_to_conversation(phone_id, [{"role": "user", "content": message}])
                else:
                    text = f"The item: {item} is not present in the inventory! Let's start over again"
                    clear_conversation(phone_id)
                    display_food_inventory(r)
            else:
                item = user_response[3:].strip()
                query_result = fetch_food_inventory_by_name(phone_id, item)
                if not query_result:
                    categories = fetch_food_inventory_categories()
                    sub_categories = fetch_food_inventory_subcategories()
                    text = f"""Alright! Adding item: {item} to inventory!\n\nPlease specify the quanity and units, and optionally a category and sub_category \n\nExisting categories: {categories}\n\nExisting sub-categories: {sub_categories}\n\n""" 
                    r.send_text(text)
                    message = f"add {item}"
                    add_msg_to_conversation(phone_id, [{"role": "user", "content": message}])
                else:
                    text = f"""The item: {item} already exists! Though you can modify it using the 'modify [item name]'""" 
                    clear_conversation(phone_id)
                    r.send_text(text)
                    display_food_inventory(r)
            r.set_bot_state("Food_Inventory_Menu")
        # 2. if conversation exists:
        elif message_history:
            # delete case:
            if message_history.messages[0]['content'].startswith("delete"):
                if user_response == "yes":
                    item = message_history.messages[0]['content'][6:].strip()
                    delete_from_food_inventory(phone_id, item)
                    text = f"item: {item} deleted from inventory!"
                    r.send_text(text)
                else:
                    r.send_text("Phew! That was close...")

            # modify case:
            elif message_history.messages[0]['content'].startswith("modify"):
                item = message_history.messages[0]['content'][6:].strip()
                agent = ConversationAgent()
                agent.init_for_json_creation(keys=["quantity", "units", "name", "category", "sub_category"], optional=["name", "category", "sub_category"])
                generated_json = agent.generate_response(user_response)
                try: 
                    dict_ = json.loads(generated_json)
                except Exception as e:
                    logging.error(e)
                    r.send_text(generated_json)
                    r.send_text("Sorry, that didn't work out as well as it appeared to me. Let's try again")
                else:
                    dict_ = update_generate_dict(dict_, agent, item)
                    update_food_inventory_item(phone_id, item, dict_)
                    r.send_text(f"Item: {item} modified in inventory!")
                    r.send_text(f"new properties:\n{dict_}")
            # add case
            elif message_history.messages[0]['content'].startswith("add"):
                item = message_history.messages[0]['content'][3:].strip()
                agent = ConversationAgent()
                agent.init_for_json_creation(keys=["quantity", "units", "category", "sub_category"], optional=["category", "sub_category"])
                generated_json = agent.generate_response(user_response)
                try: 
                    dict_ = json.loads(generated_json)
                except Exception as e:
                    logging.error(e)
                    r.send_text("Sorry, that didn't work out as well as I hoped. Let's try again")
                else:
                    dict_ = update_generate_dict(dict_, agent, item)
                    update_food_inventory_item(phone_id, item, dict_)
                    r.send_text(f"Item: {item} added in inventory!")
                    r.send_text(f"Properties:\n{dict_}")
            
            clear_conversation(phone_id)
            display_food_inventory(r)
            
        else:
            r.send_text("Not sure what that meant...I'm assuming you want to see the menu again?")
            clear_conversation(phone_id)
            display_food_inventory(r)
            

    if do_return:
        logging.info('Return: {}'.format(r.get_data()))
        return jsonify(r.get_response())