from data import extract_data,data_to_csv, decompress_data, preprocessing
from maps import  simplify_boundaries
import config
import os

#Data Work
extract_data.download_data(months_lst=config.Months)
decompress_data.decompress_raw_data()
data_to_csv.save_as_csv()
simplify_boundaries.simplify_map_geometries()
preprocessing.preprocess_data()

#Run Dash Application
exec(open(os.path.join(config.folder_dashboard,config.dashboard_filename)).read())