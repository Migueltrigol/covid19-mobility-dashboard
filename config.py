import os

#Folder paths
base_path = os.getcwd()
folder_data = os.path.join(base_path,"data")
folder_data_raw = os.path.join(base_path,"data","00_raw")
folder_data_decompressed = os.path.join(base_path,"data","01_decompressed")
folder_data_csv= os.path.join(base_path,"data","02_csv")
folder_data_preprocessed= os.path.join(base_path, "data","03_preprocessed")
folder_maps = os.path.join(base_path,"maps")
folder_assets = os.path.join(base_path,"assets")
folder_dashboard = os.path.join(base_path,"dashboard")

#File Names
csv_filename="maestra_2_mitma_municipio.csv"
input_shapefile="municipios_mitma.shp"
output_shapefile="municipios_mitma_simplified.geojson" 
csv_filename_preprocessed = "p_maestra_2_mitma_municipio.csv"
geojson_filename_preprocessed_monthly = "p_maestra_2_mitma_municipio_by_month.geojson"
dashboard_filename="dashboard.py"

#Inputs
Months=["202003","202004","202005","202006","202007"]