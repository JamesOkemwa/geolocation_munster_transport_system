from flask import Flask, render_template, jsonify, request
from shapely.geometry import mapping
from utility.helpers import bus_stops_data, find_nearest_bus_stop, get_next_bus_details
from routing.routing_functions import visualize_route

app = Flask(__name__)

# convert the bus stops geodataframe to geojson
stops_gdf = bus_stops_data()
stops_geojson = stops_gdf.to_json()

def process_coordinates(latitude, longitude):
    """
    Receives coordinates of the user position or destination and returns json response of details of the nearest bus stop
    """
    if latitude is not None and longitude is not None:
        nearest_bus_stop = find_nearest_bus_stop(latitude, longitude)

        next_bus_details = get_next_bus_details(nearest_bus_stop.get('stop_id'))

        return jsonify({
            'message': 'Coordinates received and processed successfully',
            'nearest_bus_stop': {
                'stop_id': nearest_bus_stop['stop_id'],
                'stop_name': nearest_bus_stop['stop_name'],
                'latitude': nearest_bus_stop['stop_lat'],
                'longitude': nearest_bus_stop['stop_lon'],
                'distance': nearest_bus_stop['distance']
            },
            'next_bus_details': {
                'arrival_time': next_bus_details['arrival_time'],
                'stop_headsign': next_bus_details['stop_headsign'],
                'route_id': next_bus_details['route_id']
            }
        })
    else:
        return jsonify({'error': 'Invalid coordinates'})

@app.route('/')
def index():
    return render_template('index.html', stops_geojson=stops_geojson)

@app.route('/process_user_position', methods=['POST'])
def process_user_position():
    """
    Receives the coordinates of the user position from the map and returns the details of the nearest bus stop to the html template
    """
    user_position = request.get_json()
    return process_coordinates(user_position.get("latitude"), user_position.get("longitude"))
    
@app.route('/process_destination_coordinates', methods=['POST'])
def process_destination_coordinates():
    """
    Receives the coordinates of the searched destination from the map, and returns the details of the nearest bus stop to the html template
    """
    destination_position = request.get_json()
    return process_coordinates(destination_position.get("latitude"), destination_position.get("longitude"))

@app.route('/get_route_polyline', methods=['POST'])
def get_route_polyline():
    """
    Receives the route_id of a particular line and returns the polyline representation of the route
    """
    data = request.get_json()
    route_polyline = visualize_route(data.get('route_id'))
    if route_polyline:
        return jsonify({
            "message": "Route polyline retrived successfully",
            "route_line": mapping(route_polyline)
        })
    else:
        return jsonify({
            "error": "An error occured"
        })


if __name__ == '__main__':
    app.run(debug=True)