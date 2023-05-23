import os
import config
import tarfile

def decompress_raw_data():
    """Decompresses the .tar files in \data\raw to the folder \data\decompressed
    """
    #Define file paths
    folder_data_raw = config.folder_data_raw
    folder_data_decompressed = config.folder_data_decompressed
    
    #Extract each file individually
    for filename in os.listdir(folder_data_raw): # Loop through all files in the folder
        if filename.endswith(".tar"): # Check if the file is a .tar file
            with tarfile.open(os.path.join(folder_data_raw, filename), "r") as tar: # Open the .tar file
                tar.extractall(folder_data_decompressed) # Extract the contents of the .tar file