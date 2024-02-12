import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

def read_gtfs_data():
    """
    Load bus stops data into a pandas dataframe, converts it into a geodataframe and returns the geodataframe
    """
    gtfs_file_path = 'data/gtfs/stadtwerke_feed/stops.txt'
    bus_stops_df = pd.read_csv(gtfs_file_path)
    gdf_stops = gpd.GeoDataFrame(bus_stops_df, geometry=gpd.points_from_xy(bus_stops_df['stop_lon'], bus_stops_df['stop_lat']), crs="EPSG:4326")

    return gdf_stops

def find_nearest_bus_stop(user_lat, user_long):
    """
    Takes the coordinates of the user position and returns the details of the nearest bus stop
    """
    bus_stops_gdf = read_gtfs_data()

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
