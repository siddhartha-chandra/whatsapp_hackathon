import json
from src.utils import get_buttons_from_data, display_main_menu, display_food_inventory, display_user_preferences
from src.db_utils import is_food_inventory_empty, add_to_food_inventory
from src.recommend.views import handle_request as handle_recommend_request
from src.user_defaults.views import handle_request as handle_userdefaults_request



# MAIN MENU
def handle_request(r, json_data, logging):
    logging.info('Data: {}'.format(json.dumps(json_data)))
    if (json_data["data"]["type"] == "reply"):
        reply_id = json_data["data"]["body"]["id"]

        # VIEW ITEMS
        if reply_id == "view_update":
            phone_id = json_data["caller"]["id"]
            no_data_present = is_food_inventory_empty(phone_id)
            if no_data_present:
                add_to_food_inventory(phone_id)
                r.send_text("Sample stock added in Food inventory")

            display_food_inventory(r)
        
        # MEAL RECOMMEND
        elif reply_id == "recommend":
            handle_recommend_request(r, json_data, logging)

        # USER PREFERENCES
        elif reply_id == "preferences":
            display_user_preferences(r, json_data["caller"]["id"])

        else:
            r.send_text("Invalid Request data")
        
    else:
        display_main_menu(r)