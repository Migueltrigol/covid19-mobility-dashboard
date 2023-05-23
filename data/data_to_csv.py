import os
import config
import pandas as pd

def save_as_csv():
    """Takes the files in \data\decompressed and saves them to a single csv in the \data\csv folder.
    """
    #Define file paths
    folder_data_decompressed= config.folder_data_decompressed
    folder_data_csv = config.folder_data_csv
    csv_filename = config.csv_filename
    csv_filepath= os.path.join(folder_data_csv,csv_filename)

    #Load all the files
    file_names=os.listdir(folder_data_decompressed)
    dfs=[]

    #Decompress one by one
    for file in file_names:
        file_path= os.path.join(folder_data_decompressed, file)
        df = pd.read_csv(file_path, delimiter="|", compression="gzip",low_memory=False)
        dfs.append(df)

    #Combine to a single dataframe
    df = pd.concat(dfs)

    #Save output
    df.to_csv(csv_filepath)


