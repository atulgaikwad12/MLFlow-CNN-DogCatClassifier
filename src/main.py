import mlflow
# import argparse
import os
import logging
from src.utils.common import create_directories

STAGE = "MAIN"  #Stage name for logs 
LOG_DIR = "logs"
LOG_FILENAME = "running_logs.log"

create_directories(LOG_DIR)

logging.basicConfig(
    filename=os.path.join(LOG_DIR,LOG_FILENAME),
    level=logging.INFO,
    format="[%(asctime)s: %(levelname)s: %(module)s] : %(message)s",
    filemode="a"
)

def main():
 
    with mlflow.start_run() as run:
        # mlflow.run(".","get_data",parameters={},use_conda="false") # alternate way to pass parameters
        mlflow.run(".","get_data",use_conda="false")
        mlflow.run(".","base_model_creation",use_conda="false")
        mlflow.run(".","training",use_conda="false")
    

if(__name__ == "__main__"):
    try:
        logging.info("\n*********MLFlow CNN classifier**********")
        logging.info(f">>>> Stage {STAGE} Started <<<<")
        main()
        logging.info(f">>>> Stage {STAGE} Completed <<<<")

    except Exception as e:
        logging.exception(e)
        raise e
