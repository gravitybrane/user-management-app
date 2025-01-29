from flask import Flask, request, jsonify

app = Flask(__name__)  # This initializes the Flask app

# In-memory datastore to managers
users = {}

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user_id = len(users) + 1
    users[user_id] = {
        "id": user_id,
        "name": data.get("name"),
        "email": data.get("email"),
    }
    return jsonify(users[user_id]), 201

@app.route('/users', methods=['GET'])
def get_users():
    #todo should I return a list(users) ?
    return jsonify(list(users.values())), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    user = users.get(user_id)
    if user:
        user.update({
            "name": data.get("name", user["name"]),
            "email": data.get("email", user["email"]),
        })
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        return jsonify({"message": "User deleted"}), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/')  # This defines a route for the home page ('/')
def home():
    return "Welcome to the User Management App!"  # Response when the route is accessed

if __name__ == '__main__':
    app.run(debug=True)  # Starts the app in debug mode for easier testing