from flask import Flask, render_template, request, redirect, url_for, jsonify
import uuid
import json
import requests

app = Flask(__name__)




@app.route('/')
def landing_page():
    return render_template('landing.html')





@app.route('/create_intake', methods=['GET', 'POST'])
def create_intake():
    # Read intake configuration from JSON file 
    with open("intake_config.json", "r") as f:
        intake_config = json.load(f)

    # Simulate the get intake id from Francis'API
    intake_id = str(uuid.uuid4())

    return render_template('intake.html', intake_id=intake_id, fields=intake_config['fields'])





@app.route('/submit_intake', methods=['POST'])
def submit_intake():
    # Get the form data
    data = request.form.to_dict()

    # Add the intake_id to the data dictionary
    intake_id = data.get('intake_id')
    if intake_id:
        data['intake_id'] = intake_id

    # Send the data to the external API
    response = requests.post('http://127.0.0.1:5001/create_intake', json=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Serialize the data to JSON
        json_data = json.dumps(data)
        return redirect(url_for('segments', data=json_data))  # passing data along with the route name
    else:
        return "An error occurred while submitting the form.", 500




@app.route('/segments', methods=['GET'])
def segments():
    # Get the JSON string from the query parameters
    json_data = request.args.get('data')
    
    # Deserialize the JSON string back to a dictionary
    if json_data:
        data = json.loads(json_data)
    else:
        data = {}


    # Mapping baseload types to their respective config files
    config_files = {
        'NBO Mobility': 'nbo-mob-config.json',
        'K/TRPU': 'ktrpu-config.json',
        'Geofencing': 'geofencing-config.json',
        'TOM & Account Memo': 'tom-account-memo-config.json',
        'NBO HS': 'nbo-hs-config.json'
    }

    # Get the file path based on the baseload_type
    config_file = config_files.get(data.get('baseload_type'))

    if not config_file:
        return jsonify({'error': 'Unsupported baseload type'}), 400

    try:
        # Load the appropriate config file
        with open(config_file, 'r') as f:
            segment_config = json.load(f)
        #return jsonify(segment_config)
    except FileNotFoundError:
        return jsonify({'error': 'Config file not found'}), 500
    

    return render_template('segments.html', data=data, segment_config=segment_config )










if __name__ == '__main__':
    app.run(debug=True, port=5002)
