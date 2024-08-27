from Flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os
import bcrypt

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Retrieve MongoDB URL and server port from environment variables
mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
server_port = int(os.getenv('SERVER_PORT', 5000))

# Connect to MongoDB
client = MongoClient(mongo_url)
db = client['supamenu']
collection = db['users']  # Collection for user data
login_attempts = db['login_attempts']  # Collection for login attempts

def serialize_document(document):
    """Convert a MongoDB document to a serializable format."""
    document['_id'] = str(document['_id'])  # Convert ObjectId to string
    return document

@app.route('/documents', methods=['GET'])
def get_all_documents():
    """Fetch all documents from the 'users' collection."""
    documents = collection.find()
    result = [serialize_document(doc) for doc in documents]  # Serialize each document
    return jsonify(result)

@app.route('/login', methods=['POST'])
def post_user_data():
    """Handle user login."""
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    user = collection.find_one({"email": email})

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        # Save the successful login attempt
        login_data = {
            "email": email,
            "status": "success"
        }
        login_attempts.insert_one(login_data) 
        return jsonify({"message": "Login successful"}), 200
    else:
        # Save the failed login attempt
        login_data = {
            "email": email,
            "status": "failed"
        }
        login_attempts.insert_one(login_data)
        return jsonify({"message": "Login failed"}), 401

@app.route('/register', methods=['POST'])
def register_user():
    """Handle user registration."""
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