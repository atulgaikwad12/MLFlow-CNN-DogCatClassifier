import argparse
import os
import logging
from random import seed
import tensorflow as tf
from tensorflow.python.ops.gen_math_ops import imag
from src.utils.common import create_directories, read_yaml
from src.utils.model import getCallbackList


STAGE = "Trainning" ## <<< change stage name 
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
    
    PARENT_DIR = os.path.join(
    config["data"]["unzip_data_dir"],
    config["data"]["parent_data_dir"])

    params = config["params"]

    logging.info(f"read the data from {PARENT_DIR}")

    train_dataset =  tf.keras.preprocessing.image_dataset_from_directory(
        PARENT_DIR,
        validation_split = params["validation_split"],
        subset = "training",
        seed = params["seed"],
        image_size= params["img_shape"][:-1],
        batch_size = params["batch_size"]

    )

    validation_dataset =  tf.keras.preprocessing.image_dataset_from_directory(
        PARENT_DIR,
        validation_split = params["validation_split"],
        subset = "validation",
        seed = params["seed"],
        image_size= params["img_shape"][:-1],
        batch_size = params["batch_size"]

    )

    train_data = train_dataset.prefetch(buffer_size=params["buffer_size"])
    val_data = validation_dataset.prefetch(buffer_size=params["buffer_size"])


    # Load base model

    base_model_dir = config["artifacts"]["BASE_MODEL_DIR"] 
    full_base_model_path = os.path.join(
        base_model_dir,
        config["artifacts"]["BASE_MODEL_NAME"]
    )

    logging.info(f"Loading base model from {base_model_dir}")

    classifier = tf.keras.models.load_model(full_base_model_path)

    # Training on base model 
    logging.info("Traning Started ......")

    callbacks_lst = getCallbackList(config_path)

    if(callbacks_lst is not None):
        logging.info(f"using {len(callbacks_lst)} callbacks during trainning ...")
        
        classifier.fit(train_data, epochs=params["epochs"], validation_data = val_data , callbacks=callbacks_lst)
    else:
        classifier.fit(train_data, epochs=params["epochs"], validation_data = val_data)

    trained_model_dir = config["artifacts"]["TRAINED_MODEL_DIR"]
    create_directories([trained_model_dir]) # Created dir if not exists

    full_trained_model_path = os.path.join(
        trained_model_dir,
        config["artifacts"]["TRAINED_MODEL_NAME"]
    )

    classifier.save(full_trained_model_path)

    


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