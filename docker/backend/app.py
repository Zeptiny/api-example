# Simple Python backend example using Flask
from flask import Flask, jsonify
from flask_cors import cross_origin
import random

app = Flask(__name__)

# Load usernames from file
with open('usernames.txt', 'r') as f:
    usernames = [line.strip() for line in f.readlines()]

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

@app.route('/users', methods=['GET'])
@cross_origin()
def get_users():
    users = []
    for i in range(1, 6):
        username = random.choice(usernames)
        users.append(
            {
                "id": i,
                "username": username,
                "email": f"{username}@example.com"
            }
        )
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True)