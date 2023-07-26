import os
import requests
import openai


class ConversationAgent:

    def __init__(self, messages=[]):
        bearer_token = os.getenv("BEARER_TOKEN")

        self.url = os.getenv("OZONE_URL")
        self.headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {bearer_token}',
            'Content-Type': 'application/json'
        }
        self.messages = messages
        self.model = "gpt-3.5-turbo"
        self.temperature = 0
        self.max_tokens = 500

    def trigger_stop_message(self):
        message = 'Thanks for using the Foodio assistant.'
        return message

    def get_first_meal_recommendation_questions(self):
        questions = """# 1. What is the meal type you're looking for [breakfast, lunch, dinner, snack, juice, cocktail, etc]
        # 2. How many people would be eating/drinking?
        """
        return questions

    def get_first_meal_recommendation_prompt(self):
        questions = self.get_first_meal_recommendation_questions()
        prompt = f"""Welcome to the Foodio Meal Recommendation service!
        In order for me to give you valuable meal recommendations, I will need you help with a few questions.
        Starting with these two:

        {questions}
        """
        return prompt
        
    def init_for_json_creation(self, *args, **kwargs):
        role  = "system"
        message = f""" You are a helpful assistant who can create a json object intelligently from a list of keys and a list of values supplied to you. The user should not be asked to provide any more details"""
        context = f"""The list of keys given to you is {kwargs.get("keys", None)}. Out of these, {kwargs.get("optional", None)} are optional."""
        
        self.messages = [
            {"role": role, "content": message},
            {"role": role, "content": context},
        ]



    def init_for_meal_recommendation(self, *args, **kwargs):
        role = "system"

        defaults_context = f"""
        You are a helpful assistant who recommends meals based on provided user constraints and availability of resources. 
        You currently have access to the following user defaults:
        
        diet preferences: {kwargs.get("diet_preferences", 'None')}
        diet restrictions: {kwargs.get("diet_restrictions", 'None')}
        cooking appliances: {kwargs.get("cooking_appliances", 'reasonably assume')}
        cooking utensils: {kwargs.get("utensils", 'reasonably asume')}
        location: {kwargs.get("location", '')}
        """

        food_inventory_context = f"""
        You also have access to user's food inventory as below: 

        {kwargs.get("food_inventory", 'No Data')}
        """

        message = f"""
        You have already asked the user:
        {self.get_first_meal_recommendation_questions()}

        Once the user answers, ask if they would like to change any of their defaults (i.e preferences, restrictions, cooking appliances, utensils, location)
        If they repond 'yes', ask them what they would like to change in this format:
        
            Answer only the ones that need to override defaults. 
            # 1. Any food preferences? (e.g. meat, vegetarian, vegan, carb-rich, protein-rich, oil-free, none, etc)
            # 2. Any food restrictions? (e.g. gluten-free, dairy-free, none, etc)
            # 3. A list of cooking utensils that you have (e.g. pots, pans, wok, etc).. you can also write 'reasonably assume'
            # 4. A list of cooking appliances that you have (e.g. fridge, microwave, oven, etc).. you can also write 'reasonably assume'
            # 5. What is your location? (eg. Mumbai, Maharashtra, India ; Austin, Texas, US, New York, New York, US; Edinburgh, Scotland, UK; Melbourne, Australia)

        Once the user has answered these properly, check if they have any other preferences that need to be noted down.

        Generate your meal recommendations in the following format:
            Serves: []
            Meal Type: []
            Calories: []
            Time to prepare: []
            Ingredient list: []
            Ingredients you don't currently have: []
            Instructions for preparing: []
        
        This response should prioritize what is already in the user's food inventory (which you already have access to) and preferably use ingredients that are locally produced and available in the user's location.
        
        Once recommendations have been sent, check if the user needs any more recommendations.
        
        Once user is done, your final response should include:
            'Have an enjoyable meal! Thanks for using the Foodio assisstant.'
            and ask the user to say 'done' to exit the program.
        """

        self.messages = [
            {"role": role, "content": defaults_context},
            {"role": role, "content": food_inventory_context},
            {"role": role, "content": message}
            ]

    def format_message(self, message, role):
        return {
            "role": role,
            "content": message
        }

    def gather_context(self, message):
        self.messages.append({
            "role": "user",
            "content": message
        })


    def generate_response(self, message, *args, **kwargs):
        self.gather_context(message)

        temp = kwargs.get("temperature", self.temperature)
        temp = min(max(temp, 0), 2)
        max_tokens = max(kwargs.get("max_tokens", self.max_tokens), 500)

        data = {
            "model": kwargs.get("model", self.model),
            "temperature": temp,
            "max_tokens": max_tokens,
            "messages": self.messages
        }

        response = requests.post(self.url, headers=self.headers, json=data)

        if response.status_code == 200:
            # Parse the response and extract the generated reply
            result = response.json()
            reply = result['response']['choices'][0]['message']['content']

            # Add the assistant's response to the context
            self.messages.append({
                "role": "assistant",
                "content": reply
            })

            return reply
        else:
            return "Error: Unable to generate a response."


# Example usage:
if __name__ == "__main__":
    
    # Initialize the MealRecommendationAgent
    agent = ConversationAgent()
    agent.init_for_meal_recommendation()

    print("""
    # Great! I'm happy to recommend something for you today. Can you help me answer the following to give you best recommendation:
    # 1. What is the meal type you're looking for [breakfast, lunch, dinner, snack, juice, cocktail, etc]
    # 2. How many people would be eating/drinking?
    """)

    while True:
        user_input = input("Enter your response: ")
        if user_input.lower() in {"done", "exit", "bye", "quit"}:
            break
        agent_response = agent.generate_response(user_input)
        print(f"Assistant: {agent_response}")
        if agent_response.endswith(agent.trigger_stop_message()):
            break

    # Print the conversation context
    for message in agent.messages:
        print(f"{message['role']}: {message['content']}")

