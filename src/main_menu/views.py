import json
from src.utils import get_buttons_from_data, display_main_menu, display_food_inventory

# MAIN MENU
def handle_request(r, json_data, logging):
    logging.info('Data: {}'.format(json.dumps(json_data)))
    if (json_data["data"]["type"] == "reply"):
        reply_id = json_data["data"]["body"]["id"]
        # VIEW ITEMS
        if reply_id == "view":
            display_food_inventory(r)
        # UPDATE ITEMS
        elif reply_id == "update":
            buttons = get_buttons_from_data(
                title="Food inventory update",
                button_names=["Update by category", "Main Menu"]
            )
            r.set_bot_state("Food_Update_Menu")

        # PAST MEALS
        elif reply_id == "history":
            # todo: 
            # connect to 'meal_consumed' table and view items
            pass

        # FAVORITE MEALS
        elif reply_id == "favorites":
            pass

        # MEAL RECOMMEND
        elif reply_id == "recommend":
            pass

        # RECORD A MEAL
        elif reply_id == "record":
            pass

        # USER PREFERENCES
        elif reply_id == "preferences":
            pass

        else:
            r.send_text("Invalid Request data")
        
    else:
        display_main_menu(r)