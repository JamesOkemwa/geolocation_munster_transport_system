import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString, Point

gtfs_file_path = 'data/gtfs/stadtwerke_feed/'

def read_shapes_data():
    """
    Load shapes data into a GeoDataFrame and return it.
    """
    shapes_df = pd.read_csv(gtfs_file_path + 'shapes.txt')

    # Convert to GeoDataFrame
    geometry = [Point(xy) for xy in zip(shapes_df['shape_pt_lon'], shapes_df['shape_pt_lat'])]
    gdf_shapes = gpd.GeoDataFrame(shapes_df, geometry=geometry, crs="EPSG:4326")

    return gdf_shapes

def read_trips_data():
    """
    Load trips data into a DataFrame and return it.
    """
    
    trips_df = pd.read_csv(gtfs_file_path + 'trips.txt')

    return trips_df

def read_routes_data():
    """
    Load routes data into a DataFrame and return it.
    """
    
    routes_df = pd.read_csv(gtfs_file_path + 'routes.txt')

    return routes_df

def visualize_route(route_id):
    """
    Takes a route_id and returns a polyline representing the particular route
    """
    shapes_gdf = read_shapes_data()
    trips_df = read_trips_data()
    routes_df = read_routes_data()

    # Filter trips data for the given route_id
    route_trips = trips_df[trips_df['route_id'] == route_id]

    # Filter shapes data based on the filtered trips
    route_shapes = shapes_gdf[shapes_gdf['shape_id'].isin(route_trips['shape_id'].unique())]

    # Merge shapes and routes data using trip_id
    merged_df = pd.merge(route_shapes, route_trips[['shape_id', 'trip_id']], on='shape_id', how='inner')

    # Create a GeoDataFrame for the route and convert it to a LineString
    route_gdf = gpd.GeoDataFrame(merged_df, geometry='geometry')

     # Drop duplicates based on shape_pt_sequence and sort the geodataframe to ensure correct ordering
    route_gdf = route_gdf.drop_duplicates(subset=['shape_pt_sequence'])
    route_gdf = route_gdf.sort_values(by='shape_pt_sequence')

    # Extract LineString from the GeoDataFrame
    route_line = LineString(route_gdf['geometry'])

    return route_line
