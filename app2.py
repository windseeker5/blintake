from flask import Flask, render_template, request, redirect, url_for, jsonify
import uuid
import json
import requests  # Importing requests here


app = Flask(__name__)


@app.route('/intake', methods=['GET', 'POST'])
def intake_page():
    # Read intake configuration from JSON file
    with open("intake_config.json", "r") as f:
        intake_config = json.load(f)

    # Get the unique intake ID from the API
    response = requests.post('http://127.0.0.1:5001/intake', json={})
    
    if response.status_code == 201:
        intake_data = response.json()
        intake_id = intake_data['id']
        print(f'*****   Debug - intake id = {intake_id}   *****')

    else:
        # Handle API error here
        print(f"Error getting intake ID: {response.text}")
        return "Failed to get intake ID"


    if request.method == 'POST':
        # Get all the form field values as JSON
        data = request.form.to_dict(flat=True)

        print(json.dumps(data))  # Print the form data in JSON format
        # Handle form submission

        return redirect(url_for('segments', intake_id=intake_id, _external=True))

    return render_template('intake.html', fields=intake_config['fields'])


@app.route('/segments', methods=['GET'])
def segments_page():
    intake_id = request.args.get('intake_id')
    data = request.args.get('data')

    # Load corresponding segment configuration dynamically (not shown)
    # Replace with logic to fetch relevant segment configurations based on intake_id
    segment_config = {"fields": []}  

    return render_template('segments.html', fields=segment_config['fields'], intake_id=intake_id, data=data)


if __name__ == '__main__':
    app.run(port=5002)
