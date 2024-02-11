import pandas as pd
import geopandas as gpd

def read_gtfs_data():
    """
    Load bus stops data into a pandas dataframe, converts it into a geodataframe and returns the geodataframe
    """
    gtfs_file_path = 'data/gtfs/stadtwerke_feed/stops.txt'
    bus_stops_df = pd.read_csv(gtfs_file_path)
    gdf_stops = gpd.GeoDataFrame(bus_stops_df, geometry=gpd.points_from_xy(bus_stops_df['stop_lon'], bus_stops_df['stop_lat']))

    return gdf_stops