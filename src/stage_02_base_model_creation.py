import argparse
import os
import logging
from warnings import filters  
import tensorflow as tf
from src.utils.common import create_directories, read_yaml
from src.utils.model import log_model_summary


STAGE = "BASE MODEL CREATION" ## <<< change stage name 
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
    
    params = config["params"]

    #Defining layers
    LAYERS = [
        tf.keras.layers.Input(shape=tuple(params["img_shape"])),
        tf.keras.layers.Conv2D(filters=32, kernel_size=(3,3), activation= "relu"),
        tf.keras.layers.MaxPool2D(pool_size=(2,2)),
        tf.keras.layers.Con2D(32,(3,3),activation= "relu"),
        tf.keras.layers.MaxPool2D(pool_size=(2,2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(8, activation="relu"),
        tf.keras.layers.Dense(8, activation="softmax")
    ]

    classifier = tf.keras.Sequential(LAYERS)

    # Won't be able to direclty log model summary details in file as it not returned by summary function 
    # so function log_model_summary to return detials 
    logging.info(f"Base Model Summary:\n {log_model_summary(classifier)}")

    classifier.compile(
        optimizer = tf.keras.optimizers.Adam(params["lr"]),
        loss = params["loss"],
        metrics = params["metrics"]
    )

    base_model_dir = config["artifacts"]["BASE_MODEL_DIR"]
    create_directories(base_model_dir)

    full_base_model_path = os.path.join(
        base_model_dir,
        config["artifacts"]["BASE_MODEL_NAME"]
    )

    classifier.save(full_base_model_path)
    logging.info(f"model saved at: {full_base_model_path}")




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