from flask import Blueprint, request, jsonify
from ResponseChat import ResponseChat
from src.utils import display_main_menu, get_buttons_from_data, display_food_inventory
import logging
import json
from src.llm_utils import ConversationAgent

from src.db_utils import (
    fetch_user_defaults, fetch_user_inventoryis_food_inventory_empty, 
    add_to_food_inventory, fetch_food_inventory_categories, fetch_food_inventory_by_category, 
    fetch_food_inventory_for_user, fetch_conversation
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
    r.set_bot_state("Food_Recommender")

    # workflow:
    # 1. get user_defaults
    defaults = fetch_user_defaults(phone_id)

    # 2. get user_inventory
    food_inventory = fetch_food_inventory_for_user(phone_id)

    # 3. get message_history for user from conversations tables
    message_history = fetch_conversation(phone_id)

    # 4. instantiate conversation agent and initialize for meal recommendation
    agent = ConversationAgent()

    # 4. if message_history exists, append to conversation agent else ask the first question to use and add to messages
    # message history should start from the first question that user receives from agent on whatsapp chat
    if not message_history:
        # ask first question
        first_question = agent.get_first_question(defaults)
        first_prompt = agent.get_first_meal_recommendation_prompt()
        # store question to conversations table
        # send_text(first_question)
        agent.append_history(agent.get_first_question(defaults))
    
    agent.messages += message_history
        


    # if message history exists, then the current request has a response from user
    # generate agent response for the user response and add to conversations table
    
    # set bot_state
    # check for terminal conditions for 'agent_response' and 'user_response', and if encountered, 
    # clear conversations table for given number
    # display main menu
    
    if (json_data["data"]["type"] == "reply"):
        reply_id = json_data["data"]["body"]["id"]
        title = json_data["data"]["body"]["title"]
        if reply_id == "recommend":
            # steps: 
            # 1. start conversation agent and gather context
            # 2. generate response from conversation agent
            # 3. format response
            # 4. More recommendations or back to main menu
            query_result = fetch_food_inventory_by_category(phone_id, title)
            ls = [repr(row) for row in query_result]
            r.send_list(ls)
            display_food_inventory(r)
        elif reply_id == "Main_Menu":
            display_main_menu(r)
        else:
            r.send_text("Sorry, I don't understand")
    else:
        # todo: add interaction with chatgpt here
        display_food_inventory(r)

    if do_return:
        logging.info('Return: {}'.format(r.get_data()))
        return jsonify(r.get_response())