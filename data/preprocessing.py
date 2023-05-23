import pandas as pd
import os
import geopandas as gpd
from datetime import datetime
import config

def get_month(fecha):
    month_int=int(str(fecha)[0:6])
    return month_int

def read_data(folder_path, filename):
    file_path= os.path.join(folder_path,filename)
    if ".geojson" in file_path:
        df = gpd.read_file(file_path)
    else: 
        df= pd.read_csv(file_path)
    return df

def join_data_and_map(df, gdf):
    gdf=gdf.merge(df, left_on="ID", right_on="distrito", how="left")
    return gdf

def adjust_coordinate_system(gdf,crs=4326):
    gdf = gdf.to_crs(epsg=crs)
    return gdf

def engineer_metrics(gdf):
    gdf["longitude"] = gdf.centroid.x
    gdf["latitude"] = gdf.centroid.y
    gdf["index2"]= gdf.index
    gdf["index2"] = gdf['index2'].astype(str)
    gdf["%"] = gdf["personas"]*100 / gdf.groupby(["ID","distrito","month"])["personas"].transform('sum')
    return gdf


def preprocess_data():
    """Takes the csv and the simplified maps and produce 2 files after performing transformations on them.
    These are the files that the dash app will read.
    """

    # Add fields to csv and save output
    df=read_data(folder_path=config.folder_data_csv, filename=config.csv_filename)
    df["month"]= df["fecha"].apply(get_month)
    df['date'] = df['fecha'].apply(lambda x: datetime.strptime(str(x), "%Y%m%d").date())
    df.to_csv(os.path.join(config.folder_data_preprocessed,config.csv_filename_preprocessed))

    # Group by month, bring in geometries, engineer new metrics as save output
    df_month=df.groupby(["month","distrito","numero_viajes"])["personas"].sum().to_frame("personas").reset_index(inplace=False) 
    gm=read_data(folder_path=config.folder_maps, filename=config.output_shapefile)
    gmdf=join_data_and_map(df_month, gm)
    gmdf=adjust_coordinate_system(gmdf)
    gmdf=engineer_metrics(gmdf)
    gmdf.to_file(os.path.join(config.folder_data_preprocessed, config.geojson_filename_preprocessed_monthly), driver='GeoJSON')
