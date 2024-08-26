from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os
import bcrypt

load_dotenv()

app = Flask(__name__)

mongo_url = os.getenv('MONGO_URL')
server_port = int(os.getenv('SERVER_PORT', 5000))

# Connecting to MongoDB
client = MongoClient(mongo_url)
db = client['supamenu']
collection = db['users']  
login_attempts = db['login_attempts']  

def serialize_document(document):
    """Convert a MongoDB document to a serializable format."""
    document['_id'] = str(document['_id'])  # Converting ObjectId to string
    return document

@app.route('/documents', methods=['GET'])
def get_all_documents():
    documents = collection.find()
    result = [serialize_document(doc) for doc in documents]  # Serializing each document
    return jsonify(result)

@app.route('/login', methods=['POST'])
def post_user_data():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    user = collection.find_one({"email": email})

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        # save the login attempt, if password matches
        login_data = {
            "email": email,
            "status": "success"
        }
        login_attempts.insert_one(login_data) 
        return jsonify({"message": "Login successful"}), 200
    else:
        # save the failed attempt, it passwords do not match or no user found
        login_data = {
            "email": email,
            "status": "failed"
        }
        login_attempts.insert_one(login_data)  # Insert failed login attempt into the database
        return jsonify({"message": "Login failed"}), 401
    
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    # Check if the user already exists
    if collection.find_one({"email": email}):
        return jsonify({"message": "User already exists"}), 400

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Create a new user document
    user_data = {
        "email": email,
        "password": hashed_password.decode('utf-8')
    }

    # Insert the user into the database
    collection.insert_one(user_data)

    return jsonify({"message": "User registered successfully"}), 201

if __name__ == "__main__":
    app.run(port=server_port, debug=True)