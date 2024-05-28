from flask import Flask, request, render_template, jsonify

from datetime import datetime
import json
import requests  # Assuming you have a function in fuzzy_system.py
from flask_cors import CORS
import random
import pickle

app = Flask(__name__)
CORS(app=app)
# Load past accident coordinates
with open('accident_coordinates_uk.json') as f:
    accident_data = json.load(f)

# Function to convert locations to coordinates
def get_coordinates(location):
    geolocator = Nominatim(user_agent="accident_prediction")
    loc = geolocator.geocode(location)
    return {"latitude": loc.latitude, "longitude": loc.longitude}

# Function to count accident locations on route
def count_accident_locations(source_coords, dest_coords):
    # Dummy implementation for counting accidents
    count = 0
    for accident in accident_data:
        # You need to implement actual logic based on route calculation
        count += 1
    return count

# Function to get rainfall data (dummy function, replace with actual API call)
def get_rainfall():
    # Replace with actual API call to get current rainfall data
    #https://history.openweathermap.org/data/2.5/aggregated/year?lat=35&lon=139&appid={API key}

    return random.randint(10,20)

@app.route('/')
def index():
    return render_template('accident_loc3.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        if data is None:
            raise ValueError("Invalid JSON data")
        # sourceLat = request.json['sourceLat']
        # sourceLon = request.json['sourceLon']

        # destLat = request.json['destLat']
        # destLon = request.json['destLon']
        age_driver = int(request.json.get('age_of_driver'))
        age_vehicle = int(request.json.get('age_of_vehicle'))

        no_of_accidents = int(request.json.get('num_accident_locations'))
        print(request.json,"data")

        with open('accident_ctrl.pkl', 'rb') as file:
            accident_ctrl = pickle.load(file=file)

        with open('accident_sim.pkl', 'rb') as file:
            accident_sim = pickle.load(file=file)

        print("files loaded")

        
        # source_coords = {'latitude':sourceLat, 'longitude': sourceLon }
        # dest_coords = {'latitude':destLat, 'longitude': destLon }
        

        # accident_locations = count_accident_locations(source_coords, dest_coords)
        rainfall = get_rainfall()

        time_of_day = datetime.now().hour

        print("Starting of prediction")

        accident_sim.input["age_of_driver"] = age_driver
        accident_sim.input["age_of_vehicle"] = age_vehicle
        accident_sim.input['rainfall'] = rainfall
        accident_sim.input['num_accident_locations'] = no_of_accidents
        accident_sim.input['time_of_day'] = time_of_day

        accident_sim.compute()
        
        print("predicting")
        
        return jsonify({
            'accident_probability': accident_sim.output['Accident Probability']*100,
            'status': 200
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 400
        })

if __name__ == '__main__':
    app.run(debug=True)