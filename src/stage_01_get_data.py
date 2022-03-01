import argparse
import os
# import shutil
# from tqdm import tqdm
import logging  
from src.utils.common import read_yaml, create_directories, unzip_file
from src.utils.data_processing import validate_imgdata
# import random
from urllib import request as req


STAGE = "GET_DATA" ## <<< change stage name 
LOG_DIR = "logs"
LOG_FILENAME = "running_logs.log"
logging.basicConfig(
            filename = os.path.join(LOG_DIR, LOG_FILENAME), 
            level=logging.INFO, 
            format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
            filemode="a"
            )


def main(config_path):
    ## read config files
    config = read_yaml(config_path)
    
    source_url = config["data"]["source_url"]
    local_dir = config["data"]["local_dir"]

    create_directories([local_dir])

    data_file = config["data"]["data_file"]

    # location to store fetched zipped data
    data_file_path  = os.path.join(local_dir, data_file)

    # Downloading file 
    if not os.path.isfile(data_file_path):
        logging.info("Downloading started ......")
        filename, header = req.urlretrieve(source_url, data_file_path)
        logging.info(f"{filename} created with info {header}")

    # Unzip downloaded file 
    unzip_data_dir = config["data"]["unzip_data_dir"]
    if not os.path.exists(unzip_data_dir):
        logging.info("Unzipping downloaded data file .......")
        create_directories(unzip_data_dir)
        unzip_file(source=data_file_path,dest=unzip_data_dir)
    else:
        logging.info("Data file already unzipped")


    # validating unzipped image files 
    validate_imgdata(config)

    

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config","-c",default="configs/config.yml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        main(config_path=parsed_args.config)
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e