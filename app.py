from flask import Flask, render_template, jsonify, request
import json
from utility.helpers import read_gtfs_data

app = Flask(__name__)

# convert the bus stops geodataframe to geojson
stops_gdf = read_gtfs_data()
stops_geojson = stops_gdf.to_json()

@app.route('/')
def index():
    return render_template('index.html', stops_geojson=stops_geojson)

@app.route('/process_user_position', methods=['POST'])
def process_user_position():
    user_position = request.get_json()

    return jsonify({'message': 'User position received and processed successfully'})

if __name__ == '__main__':
    app.run(debug=True)