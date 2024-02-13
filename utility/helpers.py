import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from datetime import datetime

def bus_stops_data():
    """
    Load bus stops data into a pandas dataframe, converts it into a geodataframe and returns the geodataframe
    """
    gtfs_file_path = 'data/gtfs/stadtwerke_feed/stops.txt'
    bus_stops_df = pd.read_csv(gtfs_file_path)
    gdf_stops = gpd.GeoDataFrame(bus_stops_df, geometry=gpd.points_from_xy(bus_stops_df['stop_lon'], bus_stops_df['stop_lat']), crs="EPSG:4326")

    return gdf_stops

def bus_stop_trip_times():
    """
    Merge bus stops data, trip data and stop times into one geodataframe and return the geodataframe
    """
    gtfs_file_path = 'data/gtfs/stadtwerke_feed/'

    bus_stops_gdf = bus_stops_data()
    stop_times_df = pd.read_csv(gtfs_file_path + 'stop_times.txt')
    trips_df = pd.read_csv(gtfs_file_path + 'trips.txt')

    # Convert 'stop_id' and 'trip_id' to a common data type in the dataframes DataFrames for easier merging
    bus_stops_gdf['stop_id'] = bus_stops_gdf['stop_id'].astype(str)
    stop_times_df['stop_id'] = stop_times_df['stop_id'].astype(str)
    trips_df['trip_id'] = trips_df['trip_id'].astype(str)

    # Merge stops, stop_times, and trips data
    merged_df = pd.merge(pd.merge(bus_stops_gdf, stop_times_df, on='stop_id'), trips_df, on='trip_id')

    return merged_df

def find_nearest_bus_stop(user_lat, user_long):
    """
    Takes the coordinates of the user position or user destination and returns the details of the nearest bus stop
    """
    bus_stops_gdf = bus_stops_data()

    # create a geodataframe with the user location
    user_point = Point(user_long, user_lat)
    user_gdf = gpd.GeoDataFrame(geometry=[user_point], crs=bus_stops_gdf.crs)

    # convert the coordinate system to a projected one for accurate calculation of distances
    projected_crs = 'EPSG:32632'
    user_gdf = user_gdf.to_crs(projected_crs)
    bus_stops_gdf = bus_stops_gdf.to_crs(projected_crs)

    # Calculate distances to all bus stops and find the nearest bus stop
    bus_stops_gdf['distance'] = bus_stops_gdf.geometry.distance(user_gdf.geometry.iloc[0])
    nearest_bus_stop = bus_stops_gdf.loc[bus_stops_gdf['distance'].idxmin()]

    return nearest_bus_stop

def normalize_time(time_str):
    """
    Normalize time values exceeding 24 hours that are present in the gtfs data eg 25:30:30 
    """
    hours, minutes, seconds = map(int, time_str.split(':'))
    total_seconds = hours * 3600 + minutes * 60 + seconds
    normalized_seconds = total_seconds % 86400  # Take the remainder to get seconds within a day
    return '{:02d}:{:02d}:{:02d}'.format(normalized_seconds // 3600, (normalized_seconds // 60) % 60, normalized_seconds % 60)

def get_next_bus_details(stop_id):
    """
    Returns a dictionary containing the stop time and stop headsign details of the next bus at a particular bus station
    """
    stop_id = str(stop_id)
    bus_stop_trip_times_gdf = bus_stop_trip_times()
    filtered_gdf = bus_stop_trip_times_gdf[bus_stop_trip_times_gdf['stop_id'] == stop_id]

    # Sort by 'arrival_time'
    sorted_gdf = filtered_gdf.sort_values(by='arrival_time')

    current_time = datetime.now().time()

    # Convert 'arrival_time' to time and normalize values exceeding 24 hours
    sorted_gdf['arrival_time'] = sorted_gdf['arrival_time'].apply(normalize_time)
    sorted_gdf['arrival_time'] = pd.to_datetime(sorted_gdf['arrival_time'], format='%H:%M:%S').dt.time

    # Filter rows where 'arrival_time' is later than the current time
    filtered_rows = sorted_gdf[sorted_gdf['arrival_time'] > current_time]

    # get the next bus details
    next_bus_details = filtered_rows.iloc[0]
    next_bus_details['arrival_time'] = next_bus_details['arrival_time'].strftime('%H:%M:%S')
    selected_columns = next_bus_details[['arrival_time', 'stop_headsign', 'route_id']]

    return selected_columns.to_dict()