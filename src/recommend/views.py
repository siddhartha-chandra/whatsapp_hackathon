from flask import Blueprint, request, jsonify
from ResponseChat import ResponseChat
from src.utils import display_main_menu, get_buttons_from_data, display_food_inventory
import logging
import json
from src.llm_utils import ConversationAgent

from src.db_utils import (
    fetch_user_defaults, is_food_inventory_empty, add_to_user_defaults,
    add_to_food_inventory, fetch_food_inventory_categories, fetch_food_inventory_by_category, 
    fetch_food_inventory_for_user, fetch_conversation, add_msg_to_conversation,
    update_user_conversation, clear_conversation, get_conversation_columns, get_user_defaults_columns, get_food_inventory_columns
    )

recommend_bp = Blueprint("meal_recommend", __name__)

# Food recommend menu
@recommend_bp.route('/meal_recommend', methods=['POST'])
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

    # set bot_state
    r.set_bot_state("Food_Recommender")

    # workflow:
    # 1. get user_defaults
    defaults = fetch_user_defaults(phone_id)
    if not defaults and json_data["data"]["type"] == "add_data":
        # add sample user_defaults to user_defaults table
        add_to_user_defaults(phone_id)
        defaults = fetch_user_defaults(phone_id)

    # 2. get user_inventory
    food_inventory = fetch_food_inventory_for_user(phone_id)

    # 3. get message_history for user from conversations tables
    message_history = fetch_conversation(phone_id)

    # 4. instantiate conversation agent and initialize for meal recommendation
    agent = ConversationAgent()
    d = dict()
    d['food_inventory'] = []
    for item in food_inventory:
        d['food_inventory'].append(
            f"{item.name}, {item.quantity} {item.units}"
        )
        
    if defaults:  
        if defaults.diet_preferences:
            d['diet_preferences'] = defaults.diet_preferences
        if defaults.diet_restrictions:
            d['diet_restrictions'] = defaults.diet_restrictions
        if defaults.cooking_appliances:
            d['cooking_appliances'] = defaults.cooking_appliances
        if defaults.utensils:
            d['utensils'] = defaults.utensils
        if defaults.location:
            d['location'] = defaults.location

    agent.init_for_meal_recommendation(**d)

    # 4. if message_history exists, append to conversation agent else ask the first question to use and add to messages
    # message history should start from the first question that user receives from agent on whatsapp chat
    if not message_history:
        # ask first question
        first_question = agent.get_first_meal_recommendation_questions()
        first_prompt = agent.get_first_meal_recommendation_prompt()
        
        # store question to conversations table
        messages = [agent.format_message(message=first_prompt, role="assistant")]
        add_msg_to_conversation(phone_id, messages)
        
        r.send_text(first_prompt)
    else:
        # if message history exists, then the current request has a response from user
        agent.messages += message_history.messages

        # generate agent response for the user response and add to conversations table    
        user_response  = json_data["data"]["body"]["data"]
        if user_response.lower() in {"done", "exit", "bye", "quit"}:
            # clear conversations table for given number
            clear_conversation(phone_id)
            # display main menu
            r.set_bot_state("Main_Menu")
            display_main_menu(r)
        else:
            agent_response = agent.generate_response(user_response)
            update_user_conversation(phone_id, agent.messages)
            r.send_text(agent_response)

        if agent_response.endswith(agent.trigger_stop_message()):
            # clear conversations table for given number
            clear_conversation(phone_id)
            # display main menu
            r.set_bot_state("Main_Menu")
            display_main_menu(r)


    if do_return:
        logging.info('Return: {}'.format(r.get_data()))
        return jsonify(r.get_response())