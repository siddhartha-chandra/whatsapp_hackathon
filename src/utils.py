
from ResponseChat import ButtonObject
from src.db_utils import fetch_food_inventory_categories

def get_buttons_from_data(title, button_names):
    buttons = ButtonObject(title)
    for i, button in enumerate(button_names):
        if type(button) != str:
            button = button[0]
        buttons.add_button(str(i + 1), button)
    return buttons


def display_food_inventory(r):

    list_obj = r.init_interactive("Food Stock")
    menu_section = list_obj.section("Categories")
    categories = fetch_food_inventory_categories()
    for i, category[0] in enumerate(categories):
        menu_section.add_choice(f"{i}", category[0])
    buttons = get_buttons_from_data(
        title="Food inventory",
        button_names=["View by category", "Main Menu"]
    )
    main_menu_section = list_obj.section("Main Menu")
    main_menu_section.add_choice("Main_Menu", "Main Menu", description="Main menu")
    r.set_bot_state("Food_Inventory_Menu")


def display_main_menu(r):
    list_obj = r.init_interactive("Welcome to Foodio! Check out the list below")
    menu_section = list_obj.section("Main Menu")
    menu_section.add_choice("view", "food stock", description="View food inventory")
    menu_section.add_choice("update", "update food stock", description="Update food inventory ")
    menu_section.add_choice("history", "meal history", description="view past meals consumed")
    menu_section.add_choice("favorites", "meal favorites", description="view your most frequently meals consumed")
    menu_section.add_choice("recommend", "recommend a meal", description="Recommend a meal based on your preferences")
    menu_section.add_choice("record", "record a meal", description="Record a meal that you consumed")
    menu_section.add_choice("preferences", "user preferences", description="View/Update your user preferences")
    # "Recommend nearby shops"
    # "Refrigerator cleanup"
    r.add_interactive_object(list_obj)
    r.set_bot_state("Main_Menu")