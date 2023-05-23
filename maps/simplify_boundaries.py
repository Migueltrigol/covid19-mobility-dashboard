
import os
import config
import geopandas as gpd
from shapely.geometry import shape

def simplify_map_geometries(tolerance=1000.0):
    """Takes the shapefile in the \data\map folder and simplifies the geometries to reduce their weight.
    The "tolerance" parameter determines the degree to which the boundaries are simplified.
    """

    #Define file paths
    folder_maps = config.folder_maps
    input_shapefile= config.input_shapefile
    output_shapefile= config.output_shapefile
    input_map_filepath = os.path.join(folder_maps,input_shapefile)
    output_map_filepath = os.path.join(folder_maps,output_shapefile)

    # Load the geopandas dataframe
    gdf = gpd.read_file(input_map_filepath)

    # Iterate over each geometry in the geopandas dataframe and simplify it
    for index, row in gdf.iterrows():
        geometry = row["geometry"]
        simplified_geometry = shape(geometry).simplify(tolerance, preserve_topology=True)
        gdf.at[index, "geometry"] = simplified_geometry   

    # Write the simplified geopandas dataframe to a new file
    gdf.to_file(output_map_filepath, driver='GeoJSON')