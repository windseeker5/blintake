from flask import Flask, render_template, request, redirect, url_for, jsonify
import uuid
import json
import requests

app = Flask(__name__)




@app.route('/get_intake_id', methods=['GET'])
def GetIntakeid():
    unique_id = str(uuid.uuid4())
    
    return unique_id






@app.route('/create_intake', methods=['POST'])
def print_data():
    # Get the JSON data from the request
    data = request.get_json()

    # Print the full JSON data
    print(json.dumps(data, indent=4))

    return jsonify({"message": "Data received successfully!"}), 200






if __name__ == '__main__':
    app.run(port=5001)
