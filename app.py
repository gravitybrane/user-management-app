from flask import Flask

app = Flask(__name__)  # This initializes the Flask app

@app.route('/')  # This defines a route for the home page ('/')
def home():
    return "Welcome to the User Management App!"  # Response when the route is accessed

if __name__ == '__main__':
    app.run(debug=True)  # Starts the app in debug mode for easier testing