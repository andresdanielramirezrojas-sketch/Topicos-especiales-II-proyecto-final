import geopandas as gpd
import pandas as pd

def transform_data(df):
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df.longitude, df.latitude),
        crs="EPSG:4326"
    )
    gdf["speed_knots"] = gdf["speed"] * 1.94384
    return gdf