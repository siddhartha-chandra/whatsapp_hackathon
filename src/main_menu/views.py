import json
from src.utils import get_buttons_from_data, display_main_menu, display_food_inventory
from src.db_utils import is_food_inventory_empty, add_to_food_inventory


# MAIN MENU
def handle_request(r, json_data, logging):
    logging.info('Data: {}'.format(json.dumps(json_data)))
    if (json_data["data"]["type"] == "reply"):
        reply_id = json_data["data"]["body"]["id"]

        # VIEW ITEMS
        if reply_id == "view":
            phone_id = json_data["caller"]["id"]
            no_data_present = is_food_inventory_empty(phone_id)
            if no_data_present:
                add_to_food_inventory(phone_id)
                r.send_text("Sample stock added in Food inventory")

            display_food_inventory(r)
        # UPDATE ITEMS
        elif reply_id == "update":
            buttons = get_buttons_from_data(
                title="Food inventory update",
                button_names=["Update by category", "Main Menu"]
            )
            r.set_bot_state("Food_Update_Menu")

        
        # MEAL RECOMMEND
        elif reply_id == "recommend":
            pass

        # USER PREFERENCES
        elif reply_id == "preferences":
            pass

        else:
            r.send_text("Invalid Request data")
        
    else:
        display_main_menu(r)