# Simple Python backend example using Flask
from flask import Flask, jsonify, request
from flask_cors import cross_origin
import random
import itertools
import os
from datetime import datetime

app = Flask(__name__)
start_time = datetime.now()

# Database configuration
USE_DATABASE = os.getenv('USE_DATABASE', 'false').lower() == 'true'

# Initialize database connection if enabled
db_conn = None
if USE_DATABASE:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    
    db_conn = psycopg2.connect(
        host=os.getenv('DATABASE_HOST', 'localhost'),
        port=os.getenv('DATABASE_PORT', '5432'),
        user=os.getenv('DATABASE_USER', 'admin'),
        password=os.getenv('DATABASE_PASSWORD', 'admin'),
        database=os.getenv('DATABASE_NAME', 'backend_db')
    )
    
    # Create users table if it doesn't exist
    with db_conn.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL
            )
        ''')
        db_conn.commit()

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

# In-memory storage
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
    storage_mode = "PostgreSQL" if USE_DATABASE else "In-Memory"
    data = {
        "status": "OK",
        "message": "Service is running",
        "storage": storage_mode,
        "uptime": round((datetime.now() - start_time).total_seconds())
    }
    return jsonify(data)

@app.route('/users', methods=['GET', 'POST'])
@cross_origin()
def users_collection():
    if request.method == 'GET':
        if USE_DATABASE:
            with db_conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute('SELECT * FROM users')
                users_data = cursor.fetchall()
                return jsonify([dict(user) for user in users_data])
        else:
            return jsonify([user.to_dict() for user in users])

    elif request.method == 'POST':
        data = request.get_json()
        if not data or not data.get("username") or not data.get("email"):
            return jsonify({"error": "username and email are required"}), 400

        if USE_DATABASE:
            with db_conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    'INSERT INTO users (username, email) VALUES (%s, %s) RETURNING *',
                    (data["username"], data["email"])
                )
                new_user = cursor.fetchone()
                db_conn.commit()
                return jsonify(dict(new_user)), 201
        else:
            new_user = User(
                user_id=next(user_id_counter),
                username=data["username"],
                email=data["email"]
            )
            users.append(new_user)
            return jsonify(new_user.to_dict()), 201


@app.route('/users/<int:user_id>', methods=['DELETE', 'PUT'])
@cross_origin()
def manage_user(user_id):
    if request.method == 'DELETE':
        if USE_DATABASE:
            with db_conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute('DELETE FROM users WHERE id = %s RETURNING *', (user_id,))
                deleted_user = cursor.fetchone()
                db_conn.commit()
                if deleted_user:
                    return jsonify({"message": "User deleted"}), 200
                return jsonify({"error": "User not found"}), 404
        else:
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

        if USE_DATABASE:
            with db_conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    'UPDATE users SET username = %s, email = %s WHERE id = %s RETURNING *',
                    (data["username"], data["email"], user_id)
                )
                updated_user = cursor.fetchone()
                db_conn.commit()
                if updated_user:
                    return jsonify(dict(updated_user)), 200
                return jsonify({"error": "User not found"}), 404
        else:
            for u in users:
                if u.id == user_id:
                    u.username = data["username"]
                    u.email = data["email"]
                    return jsonify(u.to_dict()), 200
            return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        if USE_DATABASE and db_conn:
            db_conn.close()
            print("Database connection closed")