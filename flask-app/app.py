import os
from datetime import datetime

from flask import Flask, jsonify, request  # Import necessary modules from Flask
from pymongo import MongoClient

# Initialize the Flask application
# The variable should be __name__ with double underscores
app = Flask(__name__)

# Set up the MongoDB client
# The MongoDB URI is fetched from the environment variable 'MONGODB_URI'
# If not found, it defaults to 'mongodb://localhost:27017/'
client = MongoClient(os.environ.get("MONGODB_URI"))


# Connect to the database named 'flask_db'
db = client.flask_db

# Connect to the collection named 'data' within the 'flask_db' database
collection = db.data  # Corrected the variable assignment here


# Define the route for the root URL
@app.route("/")
def index():
    # Return a welcome message with the current time
    return f"Welcome to the Flask app! The current time is: {datetime.now()}"


# Define the route for the '/data' endpoint
# This endpoint supports both GET and POST methods
@app.route("/data", methods=["GET", "POST"])
def data():
    if request.method == "POST":
        # If the request method is POST, get the JSON data from the request
        data = request.get_json()

        if data is None:
            # Added a check for empty/invalid JSON data
            return jsonify({"status": "Invalid JSON or no data provided"}), 400

        # Insert the data into the 'data' collection in MongoDB
        collection.insert_one(data)
        # Return a success message with status code 201 (Created)
        return jsonify({"status": "Data inserted"}), 201

    elif request.method == "GET":
        # If the request method is GET, retrieve all documents from the 'data' collection
        # Convert the documents to a list, excluding the '_id' field for JSON serialization
        data_list = list(
            collection.find({}, {"_id": 0})
        )  # Renamed data to data_list to avoid conflict
        # Return the data as a JSON response with status code 200 (OK)
        return jsonify(data_list), 200


# Run the Flask application
# The variable name must be __main__ with double underscores
if __name__ == "__main__":
    # The application will listen on all available IP addresses (0.0.0.0) and port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)  # Added debug=True for development
