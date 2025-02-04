from flask import Flask, request, jsonify
import os
from google.cloud import firestore

#Set Firestore credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "firestore-key.json"

# Initialize Firestore
db = firestore.Client(database="users")
users_ref = db.collection("users")

# Initialize the Flask app
app = Flask(__name__)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user_ref = users_ref.document()  # Auto-generate Firestore ID
    new_user_ref.set({"name": data["name"], "email": data["email"]})
    return jsonify({"id": new_user_ref.id, "name": data["name"], "email": data["email"]}), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = [doc.to_dict() | {"id": doc.id} for doc in users_ref.stream()]
    return jsonify(users), 200

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user_doc = users_ref.document(user_id).get()
    if user_doc.exists:
        return jsonify(user_doc.to_dict() | {"id": user_id}), 200
    return jsonify({"error": "User not found"}), 404

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    user_doc = users_ref.document(user_id)

    if not user_doc.get().exists:
        return jsonify({"error": "User not found"}), 404

    user_doc.update(data)
    return jsonify({"id": user_id, **data}), 200

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user_doc = users_ref.document(user_id)

    if not user_doc.get().exists:
        return jsonify({"error": "User not found"}), 404

    user_doc.delete()
    return jsonify({"message": "User deleted"}), 200

@app.route('/')  # This defines a route for the home page ('/')
def home():
    return "Welcome to the User Management App!"  # Response when the route is accessed

if __name__ == '__main__':
    app.run(debug=True)  # Starts the app in debug mode for easier testing