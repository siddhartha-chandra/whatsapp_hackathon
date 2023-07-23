from flask import Blueprint, request, jsonify
from ResponseChat import ResponseChat
from src.utils import display_main_menu, get_buttons_from_data, display_user_preferences
import logging
import json
from src.db_utils import (
    fetch_conversation, clear_conversation, add_msg_to_conversation,
    add_to_user_defaults, fetch_user_defaults, update_user_preferences, create_user_defaults
    )
from src.llm_utils import ConversationAgent

user_defaults_bp = Blueprint("user_defaults", __name__)



def reset_preference_in_query_result(preference, query_result, value=None):
    
    if preference == "diet_preferences":
        query_result.diet_preferences = value if value else []
    elif preference == "diet_restrictions":
        query_result.diet_restrictions = value if value else []
    elif preference == "cooking_appliances":
        query_result.cooking_appliances = value if value else[]
    elif preference == "utensils":
        query_result.utensils = value if value else []
    elif preference == "location":
        query_result.location = value if value else ""
    return query_result



def parse_query_result(preference, query_result):
    result = ""
    if preference == "diet_preferences":
        result = query_result.diet_preferences
    elif preference == "diet_restrictions":
        result = query_result.diet_restrictions
    elif preference == "cooking_appliances":
        result = query_result.cooking_appliances
    elif preference == "utensils":
        result = query_result.utensils
    elif preference == "location":
        result = query_result.location
    return result


# User defaults menu
@user_defaults_bp.route('/user_defaults', methods=['POST'])
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

    # add to user_defaults if needed
    if json_data["data"]["type"] == "add_data":
        # add sample user_defaults to user_defaults table
        add_to_user_defaults(phone_id)
        r.send_text("Sample user defaults added!")
        defaults = fetch_user_defaults(phone_id)


    elif (json_data["data"]["type"] == "reply"):
        reply_id = json_data["data"]["body"]["id"]
        title = json_data["data"]["body"]["title"]
        ls = []
        if reply_id == "diet_preferences":
            # show data
            query_result = fetch_user_defaults(phone_id)
            if query_result:
                result = query_result.diet_preferences if query_result.diet_preferences else []
                ls = [repr(row) for row in result]
            r.send_list(ls)
            display_user_preferences(r, phone_id)
        elif reply_id == "diet_restrictions":
            query_result = fetch_user_defaults(phone_id)
            if query_result:
                result = query_result.diet_restrictions if query_result.diet_restrictions else []
                ls = [repr(row) for row in result]
            r.send_list(ls)
            display_user_preferences(r, phone_id)
        elif reply_id == "cooking_appliances":
            query_result = fetch_user_defaults(phone_id)
            if query_result:
                result = query_result.cooking_appliances if query_result.cooking_appliances else []
                ls = [repr(row) for row in result]
            r.send_list(ls)
            display_user_preferences(r, phone_id)
        elif reply_id == "utensils":
            query_result = fetch_user_defaults(phone_id)
            if query_result:
                result = query_result.utensils if query_result.utensils else []
                ls = [repr(row) for row in result]
            r.send_list(ls)
            display_user_preferences(r, phone_id)
        elif reply_id == "location":
            query_result = fetch_user_defaults(phone_id)
            if query_result:
                result = query_result.location if query_result.location else []            
            r.send_text(result)
            display_user_preferences(r, phone_id)
        elif reply_id == "Main_Menu":
            display_main_menu(r)
        else:
            r.send_text("Invalid reply!")
    elif json_data["data"]["type"] != "reply":
        # workflow
        # this is when user wants to add/modify/delete preference in the user_preferences dataset

        # STEPS:
        # do conversation only when user data starts with 'add' or 'modify' or 'delete' there is conversational context
        message_history = fetch_conversation(phone_id)
        user_response  = json_data["data"]["body"]["data"].lower()
        
        # 1. if conversation does not exist and add/modify/delete starts the request:
        if not message_history and any(user_response.startswith(s) for s in ["add", "modify", "delete"]):
            # For modify:
            if user_response.startswith("modify"):
                preference = user_response[6:].strip()
                query_result = fetch_user_defaults(phone_id)
                result = parse_query_result(preference, query_result) if query_result else ""
        
                if result:
                    text = f"""The preference: {preference} is set and has the following properties: \n{result}"""
                    r.send_text(text)
                    text = f"""Please enter the new values for this preference in the same format as the one shown above."""
                    r.send_text(text)
                    message = f"modify {preference}"
                    add_msg_to_conversation(phone_id, [{"role": "user", "content": message}])
                else:
                    text = f"The preference: {preference} is not set! Let's start over again"
                    clear_conversation(phone_id)
                    r.send_text(text)
                    display_user_preferences(r, phone_id)
            elif user_response.startswith("delete"):
                preference = user_response[7:].strip()
                query_result = fetch_user_defaults(phone_id)
                result = parse_query_result(preference, query_result) if query_result else ""
                if result:
                    text = f"""The preference: {preference} is set and has the following value: \n{result}"""
                    r.send_text(text)
                    text = f"""Are you sure you want to delete this preference ?"""
                    r.send_text(text)
                    message = f"delete {preference}"
                    add_msg_to_conversation(phone_id, [{"role": "user", "content": message}])
                else:
                    text = f"The preference: {preference} is not set! Let's start over again"
                    clear_conversation(phone_id)
                    r.send_text(text)
                    display_user_preferences(r, phone_id)
            else:
                preference = user_response[3:].strip()
                query_result = fetch_user_defaults(phone_id)
                result = parse_query_result(preference, query_result) if query_result else ""
                if not result:
                    text = f"""Alright! Setting value for the preference: {preference}!\n\nPlease go ahead and add value/s""" 
                    r.send_text(text)
                    message = f"add {preference}"
                    add_msg_to_conversation(phone_id, [{"role": "user", "content": message}])
                else:
                    text = f"""The preference: {preference} is already set! Though you can modify it using 'modify [preference name]'""" 
                    r.send_text(text)
                    clear_conversation(phone_id)
                    display_user_preferences(r, phone_id)
        # 2. if conversation exists:
        elif message_history:
            query_result = fetch_user_defaults(phone_id)
            # delete case:
            if message_history.messages[0]['content'].startswith("delete"):
                if user_response == "yes":
                    preference = message_history.messages[0]['content'][3:].strip()
                    query_result = reset_preference_in_query_result(preference, query_result)
                    update_user_preferences(phone_id, query_result)
                    text = f"preference: {preference} has been cleared!"
                    r.send_text(text)
                else:
                    r.send_text("Phew! That was close...")

            # modify case:
            elif message_history.messages[0]['content'].startswith("modify"):
                preference = message_history.messages[0]['content'][6:].strip()
                if preference != 'location':
                    user_response = [k.strip() for k in user_response.split(",")]
                try: 
                    query_result = reset_preference_in_query_result(preference, query_result, user_response)                    
                    update_user_preferences(phone_id, query_result)
                except Exception as e:
                    logging.error(e)
                    r.send_text("Sorry, that didn't work out as well as it appeared to me. Let's try again")
                else:
                    r.send_text(f"preference: {preference} has been set!")
                    r.send_text(f"new value:\n{user_response}")
            # add case
            elif message_history.messages[0]['content'].startswith("add"):
                preference = message_history.messages[0]['content'][3:].strip()
                if preference != "location":
                    user_response = [k.strip() for k in user_response.split(",")]
                
                try: 
                    user_prefeences = create_user_defaults(phone_id)
                    user_prefeences = reset_preference_in_query_result(preference, user_prefeences, user_response)                    
                    update_user_preferences(phone_id, user_prefeences)

                except Exception as e:
                    logging.error(e)
                    r.send_text("Sorry, that didn't work out as well as it appeared to me. Let's try again")
                else:
                    r.send_text(f"preference: {preference} has been set!")
                    r.send_text(f"new value:\n{user_response}")
            
            clear_conversation(phone_id)
            display_user_preferences(r, phone_id)
            
        else:
            r.send_text("Not sure what that meant...I'm assuming you want to see the menu again?")
            display_user_preferences(r, phone_id)
            

    if do_return:
        logging.info('Return: {}'.format(r.get_data()))
        return jsonify(r.get_response())