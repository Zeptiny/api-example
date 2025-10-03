# Simple Python backend example using Flask
from flask import Flask, jsonify, request
from flask_cors import cross_origin
import random
import itertools

app = Flask(__name__)


class User:
    def __init__(self, user_id, username, email):
        self.id = user_id
        self.username = username
        self.email = email

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }

users = []
user_id_counter = itertools.count(1)

@app.route('/data', methods=['GET'])
@cross_origin()
def get_data():
    data = {
        "id": 1,
        "name": "Sample Item",
        "description": "This is a sample item."
    }
    return jsonify(data)

@app.route('/random', methods=['GET'])
@cross_origin()
def get_random_data():
    data = {
        "number": random.randint(1, 100),
        "string": ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))
    }
    return jsonify(data)

@app.route('/status', methods=['GET'])
@cross_origin()
def get_status():
    data = {
        "status": "OK",
        "message": "Service is running"
    }
    return jsonify(data)

@app.route('/users', methods=['GET', 'POST'])
@cross_origin()
def users_collection():
    if request.method == 'GET':
        return jsonify([user.to_dict() for user in users])

    elif request.method == 'POST':
        data = request.get_json()
        if not data or not data.get("username") or not data.get("email"):
            return jsonify({"error": "username and email are required"}), 400

        new_user = User(
            user_id=next(user_id_counter),
            username=data["username"],
            email=data["email"]
        )
        users.append(new_user)
        return jsonify(new_user.to_dict()), 201


@app.route('/users/<int:user_id>', methods=['DELETE', 'PUT'])
@cross_origin()
def delete_user(user_id):
    if request.method == 'DELETE':
        global users
        for u in users:
            if u.id == user_id:
                users.remove(u)
                return jsonify({"message": "User deleted"}), 200
        return jsonify({"error": "User not found"}), 404
    elif request.method == 'PUT':
        data = request.get_json()
        if not data or not data.get("username") or not data.get("email"):
            return jsonify({"error": "username and email are required"}), 400

        for u in users:
            if u.id == user_id:
                u.username = data["username"]
                u.email = data["email"]
                return jsonify(u.to_dict()), 200
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)