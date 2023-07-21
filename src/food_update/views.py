import json

def handle_request(r, json_data, logging):
    if (json_data["data"]["type"] == "reply"):
        reply_id = json_data["data"]["body"]["id"]
        if reply_id == "1":
            # show categories present
            pass
        elif reply_id == "2":
            pass
        else:
            r.send_text("Unknown event")
            r.set_bot_state("Main_Menu")
