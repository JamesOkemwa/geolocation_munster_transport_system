from flask import Flask, render_template
from utility.helpers import read_gtfs_data

app = Flask(__name__)

# convert the bus stops geodataframe to geojson
stops_gdf = read_gtfs_data()
stops_geojson = stops_gdf.to_json()
print(stops_geojson)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)