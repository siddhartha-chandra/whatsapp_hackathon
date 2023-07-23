
from ResponseChat import ButtonObject
from src.db_utils import fetch_food_inventory_categories, fetch_user_defaults

def get_buttons_from_data(title, button_names):
    buttons = ButtonObject(title)
    for i, button in enumerate(button_names):
        if type(button) != str:
            button = button[0]
        buttons.add_button(str(i + 1), button)
    return buttons

def display_user_preferences(r, phone_id):
    list_obj = r.init_interactive("User Preferences")
    menu_section = list_obj.section("Preference")
    preferences = fetch_user_defaults(phone_id)

    if preferences:
        if preferences.diet_preferences:
            menu_section.add_choice("diet_preferences", "diet preferences")
            i += 1
        if preferences.diet_restrictions:
            menu_section.add_choice(f"diet_restrictions", "diet restrictions")
            i += 1
        if preferences.cooking_appliances:
            menu_section.add_choice("cooking_appliances", "cooking appliances")
            i += 1
        if preferences.utensils:
            menu_section.add_choice(f"utensils", "cooking utensils")
            i += 1
        if preferences.location:
            menu_section.add_choice(f"location", "location")

    
    main_menu_section = list_obj.section("Main Menu")
    main_menu_section.add_choice("Main_Menu", "Main Menu", description="")
    r.add_interactive_object(list_obj)
    text = "From the interactive list above, you can view user preferences by category or return to the main menu."
    text_2 = "Alternately, if you want to add/modify/delete an item in your user preferences, please write the exact name of the item in the following format: Add/Modify/Delete [Item name]"
    r.set_bot_state("User_Preferences_Menu")

def display_food_inventory(r):

    list_obj = r.init_interactive("Food Stock")
    menu_section = list_obj.section("Categories")
    categories = fetch_food_inventory_categories()
    for i, category in enumerate(categories):
        menu_section.add_choice(f"{i}", category[0])
    
    main_menu_section = list_obj.section("Main Menu")
    main_menu_section.add_choice("Main_Menu", "Main Menu", description="")
    r.add_interactive_object(list_obj)
    r.set_bot_state("Food_Inventory_Menu")


def display_main_menu(r):
    list_obj = r.init_interactive("Welcome to Foodio! Check out the list below")
    menu_section = list_obj.section("Main Menu")
    menu_section.add_choice("recommend", "recommend a meal", description="Recommend a meal based on your preferences")
    menu_section.add_choice("preferences", "user preferences", description="View/Update your user preferences")
    r.add_interactive_object(list_obj)
    r.set_bot_state("Main_Menu")