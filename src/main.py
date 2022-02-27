import mlflow
# import argparse
import os
import logging

STAGE = "MAIN"  #Stage name for logs 

logging.basicConfig(
    filename=os.path.join("logs","running_logs.log"),
    level=logging.INFO,
    format="[%(asctime)s: %(levelname)s: %(module)s] : %(message)s",
    filemode="a"
)

def main():
    pass
    '''
    with mlflow.start_run() as run:
        #mlflow.run(".","get_data",parameters={},useConda="false")
        mlflow.run(".","get_data",useConda="false")
        mlflow.run(".","base_model_creation",useConda="false")
        mlflow.run(".","training",useConda="false")
    '''

if(__name__ == "__main__"):
    try:
        logging.info("\n*********MLFlow CNN classifier**********")
        logging.info(f">>>> Stage {STAGE} Started <<<<")
        main()
        logging.info(f">>>> Stage {STAGE} Completed <<<<")

    except Exception as e:
        logging.exception(e)
        raise e
