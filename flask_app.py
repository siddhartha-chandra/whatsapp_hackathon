from flask import Flask, jsonify
from ResponseChat import ButtonObject, ResponseChat

app = Flask(__name__)
response = ResponseChat()

@app.route('/menu', methods=['POST'])
def get_menu():
    # Create a ButtonObject
    buttons = ButtonObject("Please share your feedback on this document")
    buttons.add_button("3", "Excellent")
    buttons.add_button("2", "Good")
    buttons.add_button("1", "Poor")
    # Add the buttons to the response
    response.add_buttons(buttons)

    response_data = response.get_response()
    return jsonify(response_data)

@app.route('/')
def index():
    # A welcome message to test our server
    return "<h1>Welcome to the api!</h1>"

if __name__ == '__main__':
    app.run()

