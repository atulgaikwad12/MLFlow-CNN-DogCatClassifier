import argparse
import os
import logging
import tensorflow as tf
from src.utils.common import create_directories, read_yaml


STAGE = "Callback Addition" ## <<< change stage name 
LOG_DIR = "logs"
LOG_FILENAME = "running_logs.log"

logging.basicConfig(
            filename = os.path.join(LOG_DIR, LOG_FILENAME), 
            level=logging.DEBUG, 
            format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
            filemode="a"
            )


def main(config_path):
    ## read config files
    config = read_yaml(config_path)
    
    params = config["params"]
    # Need to add Callback part here 

    


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