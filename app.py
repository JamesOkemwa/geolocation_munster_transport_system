from flask import Flask, render_template, jsonify, request
import json
from utility.helpers import read_gtfs_data, find_nearest_bus_stop

app = Flask(__name__)

# convert the bus stops geodataframe to geojson
stops_gdf = read_gtfs_data()
stops_geojson = stops_gdf.to_json()

@app.route('/')
def index():
    return render_template('index.html', stops_geojson=stops_geojson)

@app.route('/process_user_position', methods=['POST'])
def process_user_position():
    """
    Receives the coordinates of the user position from the map and returns the details of the nearest bus stop
    """
    user_position = request.get_json()
    user_lat = user_position.get("latitude")
    user_long = user_position.get("longitude")

    if user_lat is not None and user_long is not None:
        nearest_bus_stop = find_nearest_bus_stop(user_lat, user_long)

        return jsonify({
            'message': 'User position received and processed successfully',
            'nearest_bus_stop': {
                'stop_id': nearest_bus_stop['stop_id'],
                'stop_name': nearest_bus_stop['stop_name'],
                'latitude': nearest_bus_stop['stop_lat'],
                'longitude': nearest_bus_stop['stop_lon'],
                'distance': nearest_bus_stop['distance']
            }
        })
    else:
        return jsonify({ 'error': 'Invalid user position'})
    
@app.route('/process_destination_coordinates', methods=['POST'])
def process_destination_coordinates():
    """
    Receives the coordinates of the searched destination, and returns the details of the nearest bus stop
    """
    destination_position = request.get_json()
    destination_lat = destination_position.get("latitude")
    destination_long = destination_position.get("longitude")

    if destination_lat is not None and destination_long is not None:
        nearest_bus_stop = find_nearest_bus_stop(destination_lat, destination_long)
        print(nearest_bus_stop)

        return jsonify({
            'message': 'User position received and processed successfully',
            'nearest_bus_stop': {
                'stop_id': nearest_bus_stop['stop_id'],
                'stop_name': nearest_bus_stop['stop_name'],
                'latitude': nearest_bus_stop['stop_lat'],
                'longitude': nearest_bus_stop['stop_lon'],
                'distance': nearest_bus_stop['distance']
            }
        })
    else:
        return jsonify({ 'error': 'Invalid destination coordinates'})


if __name__ == '__main__':
    app.run(debug=True)